import { test, expect } from '@playwright/test';

test.describe('Delete Incident', () => {
  test('should allow owner to delete their incident', async ({ page }) => {
    const userId = 'test-user-123';
    
    // Set mock user ID in localStorage
    await page.goto('/incidents');
    await page.evaluate((id) => {
      localStorage.setItem('mock_user_id', id);
    }, userId);

    // Mock the list API with an incident owned by current user
    await page.route('**/api/v1/incidents*', async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify([
            {
              id: 'incident-to-delete',
              title: 'Test Incident',
              description: 'This will be deleted',
              category: 'MAINTENANCE',
              created_at: new Date().toISOString(),
              owner_id: userId
            }
          ]),
        });
      }
    });

    await page.goto('/incidents');
    
    // Verify incident is visible
    await expect(page.getByText('Test Incident')).toBeVisible();
    
    // Verify delete button is visible (owner)
    const deleteButton = page.getByLabel('Delete incident');
    await expect(deleteButton).toBeVisible();

    // Mock the delete API
    await page.route('**/api/v1/incidents/incident-to-delete', async (route) => {
      if (route.request().method() === 'DELETE') {
        await route.fulfill({
          status: 204,
        });
      }
    });

    // Mock the list API to return empty after delete
    let deleteHappened = false;
    await page.route('**/api/v1/incidents*', async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify(deleteHappened ? [] : [
            {
              id: 'incident-to-delete',
              title: 'Test Incident',
              description: 'This will be deleted',
              category: 'MAINTENANCE',
              created_at: new Date().toISOString(),
              owner_id: userId
            }
          ]),
        });
      }
    });

    await page.route('**/api/v1/incidents/incident-to-delete', async (route) => {
      if (route.request().method() === 'DELETE') {
        deleteHappened = true;
        await route.fulfill({
          status: 204,
        });
      }
    });

    // Click delete button
    await deleteButton.click();

    // Verify dialog appears
    await expect(page.getByText('Delete Incident')).toBeVisible();
    await expect(page.getByText(/Are you sure you want to delete/)).toBeVisible();

    // Click confirm
    await page.getByRole('button', { name: 'Delete' }).click();

    // Wait a moment for the mutation to complete
    await page.waitForTimeout(500);

    // Verify incident is removed from list
    await expect(page.getByText('No incidents reported')).toBeVisible();
  });

  test('should not show delete button for non-owner', async ({ page }) => {
    const ownerId = 'owner-123';
    const currentUserId = 'other-user-456';
    
    // Set different user ID
    await page.goto('/incidents');
    await page.evaluate((id) => {
      localStorage.setItem('mock_user_id', id);
    }, currentUserId);

    // Mock API with incident owned by someone else
    await page.route('**/api/v1/incidents*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 'other-incident',
            title: 'Someone Else\'s Incident',
            description: 'Not mine',
            category: 'CLEANING',
            created_at: new Date().toISOString(),
            owner_id: ownerId
          }
        ]),
      });
    });

    await page.goto('/incidents');

    // Verify incident is visible
    await expect(page.getByText('Someone Else\'s Incident')).toBeVisible();
    
    // Verify delete button is NOT visible
    await expect(page.getByLabel('Delete incident')).not.toBeVisible();
  });
});
