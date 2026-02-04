import { test, expect } from '@playwright/test';

test.describe('Create Incident', () => {
  test('should allow creating a new incident', async ({ page }) => {
    // Mock API
    await page.route('**/api/v1/incidents', async route => {
      const json = { id: '123', title: 'Broken Elevator', status: 'OPEN' };
      await route.fulfill({ json });
    });

    await page.goto('/incidents/new');

    // Check title
    await expect(page.locator('h3', { hasText: 'Report New Incident' })).toBeVisible();

    // Fill form
    await page.getByLabel('Title').fill('Broken Elevator');
    
    // Select Category (Radix UI Select is tricky, usually hidden input or specialized click)
    // Radix Select trigger has role 'combobox'? No, it uses a button trigger.
    await page.getByRole('combobox').click();
    await page.getByRole('option', { name: 'MAINTENANCE' }).click(); // Default is Maintenance, maybe select NOISE to change?
    // Let's select SECURITY to verify change
    await page.getByRole('combobox').click(); 
    await page.getByRole('option', { name: 'SECURITY' }).click();

    await page.getByLabel('Description').fill('The elevator in block A is stuck.');

    // Submit
    await page.getByRole('button', { name: 'Submit Report' }).click();

    // Verify redirection
    await expect(page).toHaveURL(/\/incidents/);
    
    // Or verify success toast/message if on same page
    // The code redirects to /incidents.
  });

  test('should show validation errors', async ({ page }) => {
    await page.goto('/incidents/new');
    await page.getByRole('button', { name: 'Submit Report' }).click();

    // Expect errors
    await expect(page.getByText('Title is required')).toBeVisible();
    await expect(page.getByText('Description is required')).toBeVisible();
  });
});
