import { test, expect } from '@playwright/test';

test.describe('Incident List', () => {
  test('should display a list of incidents', async ({ page }) => {
    // Mock the API response
    await page.route('**/api/v1/incidents*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: '1',
            title: 'Mock Incident 1',
            description: 'Description 1',
            category: 'MAINTENANCE',
            created_at: new Date().toISOString(),
            owner_id: 'user-1'
          },
          {
            id: '2',
            title: 'Mock Incident 2',
            description: 'Description 2',
            category: 'NOISE',
            created_at: new Date(Date.now() - 3600000).toISOString(),
            owner_id: 'user-2'
          }
        ]),
      });
    });

    await page.goto('/incidents');

    // Check if incidents are displayed
    await expect(page.getByText('Mock Incident 1')).toBeVisible();
    await expect(page.getByText('MAINTENANCE')).toBeVisible();
    
    await expect(page.getByText('Mock Incident 2')).toBeVisible();
    await expect(page.getByText('NOISE')).toBeVisible();
  });

  test('should display empty state when no incidents found', async ({ page }) => {
    await page.route('**/api/v1/incidents*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([]),
      });
    });

    await page.goto('/incidents');
    await expect(page.getByText('No incidents reported')).toBeVisible();
  });
});
