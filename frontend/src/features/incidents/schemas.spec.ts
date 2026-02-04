import { describe, it, expect } from 'vitest';
import { createIncidentSchema } from './schemas';

describe('createIncidentSchema', () => {
  it('should validate valid input', () => {
    const valid = {
      title: 'Valid Title',
      description: 'Valid Description',
      category: 'MAINTENANCE',
    };
    const result = createIncidentSchema.safeParse(valid);
    expect(result.success).toBe(true);
  });

  it('should fail if title is missing', () => {
    const invalid = {
      title: '',
      description: 'Valid Description',
      category: 'MAINTENANCE',
    };
    const result = createIncidentSchema.safeParse(invalid);
    expect(result.success).toBe(false);
    if (!result.success) {
        expect(result.error.flatten().fieldErrors.title).toContain('Title is required');
    }
  });

  it('should fail if description is missing', () => {
    const invalid = {
      title: 'Valid',
      description: '',
      category: 'MAINTENANCE',
    };
    const result = createIncidentSchema.safeParse(invalid);
    expect(result.success).toBe(false);
  });
});
