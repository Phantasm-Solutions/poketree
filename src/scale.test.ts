import { expect, test } from 'vitest';
import { integerFit } from './scale';

test('zoom is a whole number and never below 1', () => {
  expect(integerFit(390, 844)).toEqual({ zoom: 1, width: 390, height: 844 });
  expect(integerFit(1920, 1080)).toEqual({ zoom: 4, width: 480, height: 270 });
  expect(integerFit(100, 100).zoom).toBe(1);
});
