// Enhanced Inventory Management System

// Inventory data - Starting empty (no pre-loaded items)
let inventory = [];
let nextId = 1;

// DOM Elements
const inventoryForm = document.getElementById('inventoryForm');
const editForm = document.getElementById('editForm');
const editModal = document.getElementById('editModal');
const closeModal = document.getElementById('closeModal');
const cancelEdit = document.getElementById('cancelEdit');
const resetBtn = document.getElementById('resetBtn');
const searchInput = document.getElementById('search');
const searchBtn = document.getElementById('searchBtn');
const inventoryTable = document.getElementById('inventoryTable').getElementsByTagName('tbody')[0];

// Stats elements
const totalItemsElement = document.getElementById('totalItems');
const totalValueElement = document.getElementById('totalValue');
const lowStockElement = document.getElementById('lowStock');
const currentDateElement = document.getElementById('currentDate');

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    displayInventory();
    updateStats();
    
    // Set current date in footer
    updateCurrentDate();
});

// Update current date in footer
function updateCurrentDate() {
    const today = new Date();
    const dateString = today.toLocaleDateString('en-US', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    currentDateElement.textContent = dateString;
}

// Form submission for adding new item
inventoryForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const name = document.getElementById('name').value.trim();
    const category = document.getElementById('category').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    const price = parseFloat(document.getElementById('price').value);
    const reorderLevel = parseInt(document.getElementById('reorder').value) || 10;
    
    // Validate
    if (!name || !category || isNaN(quantity) || isNaN(price)) {
        showAlert('Please fill in all required fields correctly.', 'error');
        return;
    }
    
    if (quantity < 0) {
        showAlert('Quantity cannot be negative.', 'error');
        return;
    }
    
    if (price < 0) {
        showAlert('Price cannot be negative.', 'error');
        return;
    }
    
    // Check if item already exists
    const existingItem = inventory.find(item => 
        item.name.toLowerCase() === name.toLowerCase() && 
        item.category === category
    );
    
    if (existingItem) {
        if (confirm(`"${name}" already exists in inventory. Would you like to update the quantity instead?`)) {
            existingItem.quantity += quantity;
            showAlert(`Updated quantity of "${name}" to ${existingItem.quantity}.`, 'success');
            displayInventory();
            updateStats();
            inventoryForm.reset();
            return;
        } else {
            return;
        }
    }
    
    // Create new item
    const newItem = {
        id: nextId++,
        name,
        category,
        quantity,
        price,
        reorderLevel,
        dateAdded: new Date().toLocaleDateString()
    };
    
    // Add to inventory
    inventory.push(newItem);
    
    // Show success message
    showAlert(`"${name}" has been added to inventory successfully!`, 'success');
    
    // Reset form
    inventoryForm.reset();
    
    // Update display
    displayInventory();
    updateStats();
});

// Reset form
resetBtn.addEventListener('click', function() {
    inventoryForm.reset();
    showAlert('Form cleared.', 'info');
});

// Search functionality
searchInput.addEventListener('input', function() {
    displayInventory();
});

searchBtn.addEventListener('click', function() {
    displayInventory();
});

// Display inventory in table
function displayInventory() {
    const searchTerm = searchInput.value.toLowerCase();
    
    // Filter inventory based on search
    const filteredInventory = inventory.filter(item => {
        return item.name.toLowerCase().includes(searchTerm) || 
               item.category.toLowerCase().includes(searchTerm);
    });
    
    // Clear table
    inventoryTable.innerHTML = '';
    
    // If no items match search
    if (filteredInventory.length === 0) {
        const row = document.createElement('tr');
        if (inventory.length === 0) {
            row.innerHTML = `
                <td colspan="7" style="text-align: center; padding: 40px; color: #777;">
                    <i class="fas fa-box-open" style="font-size: 2rem; margin-bottom: 10px; display: block;"></i>
                    Your inventory is empty. Add your first item to get started!
                </td>
            `;
        } else {
            row.innerHTML = `
                <td colspan="7" style="text-align: center; padding: 40px; color: #777;">
                    <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 10px; display: block;"></i>
                    No items found matching "${searchTerm}". Try a different search term.
                </td>
            `;
        }
        inventoryTable.appendChild(row);
        return;
    }
    
    // Add rows for each item
    filteredInventory.forEach(item => {
        const row = document.createElement('tr');
        const totalValue = item.quantity * item.price;
        const isLowStock = item.quantity <= item.reorderLevel;
        
        row.innerHTML = `
            <td><strong>${item.name}</strong></td>
            <td><span class="category-badge">${item.category}</span></td>
            <td class="quantity-cell ${isLowStock ? 'low-stock' : ''}">${item.quantity}</td>
            <td class="price-cell">Ksh ${item.price.toFixed(2)}</td>
            <td>Ksh ${totalValue.toFixed(2)}</td>
            <td>
                <span class="status ${isLowStock ? 'status-low' : 'status-ok'}">
                    ${isLowStock ? '<i class="fas fa-exclamation-triangle"></i> Low Stock' : '<i class="fas fa-check-circle"></i> In Stock'}
                </span>
            </td>
            <td class="actions-cell">
                <button class="action-btn edit-btn" onclick="openEditModal(${item.id})">
                    <i class="fas fa-edit"></i> Edit
                </button>
                <button class="action-btn delete-btn" onclick="deleteItem(${item.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
            </td>
        `;
        inventoryTable.appendChild(row);
    });
}

// Update statistics
function updateStats() {
    const totalItems = inventory.length;
    const totalValue = inventory.reduce((sum, item) => sum + (item.quantity * item.price), 0);
    const lowStockItems = inventory.filter(item => item.quantity <= item.reorderLevel).length;
    
    // Update stats cards
    totalItemsElement.textContent = totalItems;
    totalValueElement.textContent = `Ksh ${totalValue.toFixed(2)}`;
    lowStockElement.textContent = lowStockItems;
}

// Delete item
function deleteItem(id) {
    const itemIndex = inventory.findIndex(item => item.id === id);
    const itemName = inventory[itemIndex].name;
    
    if (!confirm(`Are you sure you want to delete "${itemName}" from inventory?`)) return;
    
    // Remove from inventory
    inventory.splice(itemIndex, 1);
    
    // Show message
    showAlert(`"${itemName}" has been deleted from inventory.`, 'warning');
    
    // Update display
    displayInventory();
    updateStats();
}

// Open edit modal
function openEditModal(id) {
    const item = inventory.find(item => item.id === id);
    
    if (!item) return;
    
    // Populate form
    document.getElementById('editId').value = item.id;
    document.getElementById('editName').value = item.name;
    document.getElementById('editCategory').value = item.category;
    document.getElementById('editQuantity').value = item.quantity;
    document.getElementById('editPrice').value = item.price;
    document.getElementById('editReorder').value = item.reorderLevel;
    
    // Show modal
    editModal.style.display = 'flex';
}

// Close edit modal
closeModal.addEventListener('click', function() {
    editModal.style.display = 'none';
});

cancelEdit.addEventListener('click', function() {
    editModal.style.display = 'none';
});

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    if (e.target === editModal) {
        editModal.style.display = 'none';
    }
});

// Handle edit form submission
editForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form values
    const id = parseInt(document.getElementById('editId').value);
    const name = document.getElementById('editName').value.trim();
    const category = document.getElementById('editCategory').value;
    const quantity = parseInt(document.getElementById('editQuantity').value);
    const price = parseFloat(document.getElementById('editPrice').value);
    const reorderLevel = parseInt(document.getElementById('editReorder').value);
    
    // Validate
    if (!name || !category || isNaN(quantity) || isNaN(price) || isNaN(reorderLevel)) {
        showAlert('Please fill in all fields correctly.', 'error');
        return;
    }
    
    if (quantity < 0) {
        showAlert('Quantity cannot be negative.', 'error');
        return;
    }
    
    if (price < 0) {
        showAlert('Price cannot be negative.', 'error');
        return;
    }
    
    // Update item
    const itemIndex = inventory.findIndex(item => item.id === id);
    inventory[itemIndex] = {
        ...inventory[itemIndex],
        name,
        category,
        quantity,
        price,
        reorderLevel
    };
    
    // Close modal
    editModal.style.display = 'none';
    
    // Show message
    showAlert(`"${name}" has been updated successfully!`, 'success');
    
    // Update display
    displayInventory();
    updateStats();
});

// Show alert message
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlert = document.querySelector('.alert');
    if (existingAlert) existingAlert.remove();
    
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">&times;</button>
    `;
    
    // Add styles
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 6px;
        color: white;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1001;
        display: flex;
        justify-content: space-between;
        align-items: center;
        min-width: 300px;
        max-width: 400px;
        animation: slideIn 0.3s ease;
    `;
    
    // Set color based on type
    if (type === 'success') alert.style.backgroundColor = '#2ecc71';
    if (type === 'error') alert.style.backgroundColor = '#e74c3c';
    if (type === 'warning') alert.style.backgroundColor = '#f39c12';
    if (type === 'info') alert.style.backgroundColor = '#3498db';
    
    // Add to page
    document.body.appendChild(alert);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alert.parentElement) alert.remove();
    }, 5000);
}

// Export inventory data (mock functionality)
function exportData() {
    if (inventory.length === 0) {
        showAlert('No inventory data to export.', 'error');
        return;
    }
    
    const dataStr = JSON.stringify(inventory, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `inventory-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    showAlert('Inventory data exported successfully!', 'success');
}

// Add export button to UI
const exportBtn = document.createElement('button');
exportBtn.className = 'btn btn-secondary';
exportBtn.innerHTML = '<i class="fas fa-download"></i> Export Data';
exportBtn.style.marginTop = '10px';
exportBtn.onclick = exportData;

// Add to form actions
document.querySelector('.form-actions').appendChild(exportBtn);

// Add CSS for alert animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .alert button {
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        margin-left: 15px;
    }
    
    .category-badge {
        display: inline-block;
        padding: 4px 10px;
        background: #e0e0e0;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status {
        padding: 5px 10px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-ok {
        background: #d4edda;
        color: #155724;
    }
    
    .status-low {
        background: #f8d7da;
        color: #721c24;
    }
`;
document.head.appendChild(style);

// Import inventory data functionality
function importData() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    
    input.onchange = function(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const reader = new FileReader();
        reader.onload = function(event) {
            try {
                const importedData = JSON.parse(event.target.result);
                
                // Validate imported data
                if (!Array.isArray(importedData)) {
                    throw new Error('Invalid data format');
                }
                
                // Merge with existing inventory
                importedData.forEach(item => {
                    // Check if item already exists
                    const existingItemIndex = inventory.findIndex(existing => 
                        existing.name === item.name && existing.category === item.category
                    );
                    
                    if (existingItemIndex !== -1) {
                        // Update existing item
                        inventory[existingItemIndex].quantity += item.quantity || 0;
                    } else {
                        // Add new item with new ID
                        item.id = nextId++;
                        inventory.push(item);
                    }
                });
                
                showAlert(`Successfully imported ${importedData.length} items.`, 'success');
                displayInventory();
                updateStats();
                
            } catch (error) {
                showAlert('Error importing data. Please check the file format.', 'error');
            }
        };
        
        reader.readAsText(file);
    };
    
    input.click();
}

// Add import button to UI
const importBtn = document.createElement('button');
importBtn.className = 'btn btn-secondary';
importBtn.innerHTML = '<i class="fas fa-upload"></i> Import Data';
importBtn.style.marginTop = '10px';
importBtn.style.marginLeft = '10px';
importBtn.onclick = importData;

// Add to form actions
document.querySelector('.form-actions').appendChild(importBtn);