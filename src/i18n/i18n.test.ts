import { expect, test } from 'vitest';
import en from './en.json';
import ar from './ar.json';

test('en and ar have the same keys, none empty', () => {
  expect(Object.keys(ar).sort()).toEqual(Object.keys(en).sort());
  for (const v of [...Object.values(en), ...Object.values(ar)]) expect(v.trim()).not.toBe('');
});
