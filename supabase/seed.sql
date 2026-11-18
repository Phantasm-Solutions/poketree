insert into public.clubs (slug, name_en, name_ar)
values ('ngsc', 'New Giza Sporting Club', 'نادي نيو جيزة الرياضي')
on conflict (slug) do nothing;
