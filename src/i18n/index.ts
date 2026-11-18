import en from './en.json';
import ar from './ar.json';

export type Lang = 'en' | 'ar';
export type Key = keyof typeof en;

export const strings: Record<Lang, Record<Key, string>> = { en, ar };

let lang: Lang = 'en';

export const getLang = (): Lang => lang;
export const isRtl = (): boolean => lang === 'ar';
export const t = (key: Key): string => strings[lang][key];

export function setLang(next: Lang): void {
  lang = next;
  document.documentElement.lang = next;
  document.documentElement.dir = isRtl() ? 'rtl' : 'ltr';
}
