// Test script to verify refresh button functionality
console.log('Testing refresh button functionality...');

// Simulate the refresh button click
function testRefreshButton() {
  console.log('1. Testing refresh button click...');
  
  // Find the refresh button
  const refreshBtn = document.querySelector('.refresh-btn');
  if (refreshBtn) {
    console.log('✅ Refresh button found');
    console.log('2. Clicking refresh button...');
    refreshBtn.click();
    
    // Check if modal appears
    setTimeout(() => {
      const modal = document.querySelector('[style*="z-index: 9999"]');
      if (modal) {
        console.log('✅ Modal appeared successfully');
        
        // Test cancel button
        const cancelBtn = modal.querySelector('button:contains("Cancel")');
        if (cancelBtn) {
          console.log('3. Testing cancel button...');
          cancelBtn.click();
          setTimeout(() => {
            if (!document.querySelector('[style*="z-index: 9999"]')) {
              console.log('✅ Cancel button works - modal closed');
            } else {
              console.log('❌ Cancel button failed - modal still open');
            }
          }, 100);
        }
        
        // Test confirm button
        setTimeout(() => {
          const confirmBtn = modal.querySelector('button:contains("Yes, Refresh")');
          if (confirmBtn) {
            console.log('4. Testing confirm button...');
            console.log('⚠️ This will reload the page - test will end here');
            // confirmBtn.click(); // Uncomment to test actual refresh
          }
        }, 200);
        
      } else {
        console.log('❌ Modal did not appear');
      }
    }, 100);
    
  } else {
    console.log('❌ Refresh button not found');
  }
}

// Run test when page loads
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', testRefreshButton);
} else {
  testRefreshButton();
}

console.log('Refresh button test script loaded'); 