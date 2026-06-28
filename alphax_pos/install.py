from __future__ import annotations

import json
import frappe

THEMES = [
 {
  "theme_id": "majlis-green",
  "theme_name": "Majlis Green",
  "theme_name_ar": "الأخضر المجلسي",
  "base": "warm",
  "vertical_tag": "restaurant",
  "is_preset": 1,
  "brand": "#0B6B5B",
  "brand_deep": "#084A3F",
  "accent": "#B8860B",
  "accent_deep": "#8A6608",
  "tokens_json": "{\"--canvas\": \"#F6F4EF\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFECE4\", \"--surface-3\": \"#E7E2D7\", \"--ink\": \"#1C1A17\", \"--ink-muted\": \"#6B6760\", \"--ink-faint\": \"#9A958C\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#0B6B5B\", \"--brand-deep\": \"#084A3F\", \"--accent\": \"#B8860B\", \"--accent-deep\": \"#8A6608\", \"--brand-tint\": \"color-mix(in srgb, #0B6B5B 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #B8860B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "riyadh-sand",
  "theme_name": "Riyadh Sand",
  "theme_name_ar": "رمال الرياض",
  "base": "warm",
  "vertical_tag": "cafe",
  "is_preset": 1,
  "brand": "#B5562C",
  "brand_deep": "#8F3F1C",
  "accent": "#3E7C4E",
  "accent_deep": "#2C5A38",
  "tokens_json": "{\"--canvas\": \"#F6F4EF\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFECE4\", \"--surface-3\": \"#E7E2D7\", \"--ink\": \"#1C1A17\", \"--ink-muted\": \"#6B6760\", \"--ink-faint\": \"#9A958C\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#B5562C\", \"--brand-deep\": \"#8F3F1C\", \"--accent\": \"#3E7C4E\", \"--accent-deep\": \"#2C5A38\", \"--brand-tint\": \"color-mix(in srgb, #B5562C 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #3E7C4E 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "espresso",
  "theme_name": "Espresso",
  "theme_name_ar": "إسبريسو",
  "base": "darkwarm",
  "vertical_tag": "cafe",
  "is_preset": 1,
  "brand": "#C8884A",
  "brand_deep": "#9A6630",
  "accent": "#E5C07B",
  "accent_deep": "#B8923F",
  "tokens_json": "{\"--canvas\": \"#16120E\", \"--surface\": \"#211C16\", \"--surface-2\": \"#2A241C\", \"--surface-3\": \"#362E23\", \"--ink\": \"#F3EFE8\", \"--ink-muted\": \"#ABA499\", \"--ink-faint\": \"#6F695E\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#C8884A\", \"--brand-deep\": \"#9A6630\", \"--accent\": \"#E5C07B\", \"--accent-deep\": \"#B8923F\", \"--brand-tint\": \"color-mix(in srgb, #C8884A 12%, #211C16)\", \"--accent-tint\": \"color-mix(in srgb, #E5C07B 16%, #211C16)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "royal-purple",
  "theme_name": "Royal Purple",
  "theme_name_ar": "الأرجواني الملكي",
  "base": "pure",
  "vertical_tag": "restaurant",
  "is_preset": 1,
  "brand": "#6D3BD1",
  "brand_deep": "#4E2796",
  "accent": "#D1A33B",
  "accent_deep": "#A37C26",
  "tokens_json": "{\"--canvas\": \"#F7F7F8\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFEFF1\", \"--surface-3\": \"#E3E3E6\", \"--ink\": \"#18181B\", \"--ink-muted\": \"#5C5C61\", \"--ink-faint\": \"#9A9AA0\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.14)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#6D3BD1\", \"--brand-deep\": \"#4E2796\", \"--accent\": \"#D1A33B\", \"--accent-deep\": \"#A37C26\", \"--brand-tint\": \"color-mix(in srgb, #6D3BD1 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #D1A33B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "ocean-teal",
  "theme_name": "Ocean Teal",
  "theme_name_ar": "الفيروزي",
  "base": "cool",
  "vertical_tag": "restaurant",
  "is_preset": 1,
  "brand": "#0E8C8C",
  "brand_deep": "#0A6868",
  "accent": "#F2784B",
  "accent_deep": "#C85A33",
  "tokens_json": "{\"--canvas\": \"#F3F6F9\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#E9EEF3\", \"--surface-3\": \"#DCE4EC\", \"--ink\": \"#15191F\", \"--ink-muted\": \"#5C636E\", \"--ink-faint\": \"#93999F\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#0E8C8C\", \"--brand-deep\": \"#0A6868\", \"--accent\": \"#F2784B\", \"--accent-deep\": \"#C85A33\", \"--brand-tint\": \"color-mix(in srgb, #0E8C8C 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #F2784B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "crimson",
  "theme_name": "Crimson",
  "theme_name_ar": "القرمزي",
  "base": "warm",
  "vertical_tag": "restaurant",
  "is_preset": 1,
  "brand": "#C0322E",
  "brand_deep": "#931F1C",
  "accent": "#C8923B",
  "accent_deep": "#9A6E26",
  "tokens_json": "{\"--canvas\": \"#F6F4EF\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFECE4\", \"--surface-3\": \"#E7E2D7\", \"--ink\": \"#1C1A17\", \"--ink-muted\": \"#6B6760\", \"--ink-faint\": \"#9A958C\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#C0322E\", \"--brand-deep\": \"#931F1C\", \"--accent\": \"#C8923B\", \"--accent-deep\": \"#9A6E26\", \"--brand-tint\": \"color-mix(in srgb, #C0322E 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #C8923B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "indigo-amber",
  "theme_name": "Indigo Amber",
  "theme_name_ar": "النيلي الكهرماني",
  "base": "cool",
  "vertical_tag": "retail",
  "is_preset": 1,
  "brand": "#3F4DB5",
  "brand_deep": "#2A3585",
  "accent": "#E0A53B",
  "accent_deep": "#B07E22",
  "tokens_json": "{\"--canvas\": \"#F3F6F9\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#E9EEF3\", \"--surface-3\": \"#DCE4EC\", \"--ink\": \"#15191F\", \"--ink-muted\": \"#5C636E\", \"--ink-faint\": \"#93999F\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#3F4DB5\", \"--brand-deep\": \"#2A3585\", \"--accent\": \"#E0A53B\", \"--accent-deep\": \"#B07E22\", \"--brand-tint\": \"color-mix(in srgb, #3F4DB5 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #E0A53B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "slate-pro",
  "theme_name": "Slate Pro",
  "theme_name_ar": "رمادي احترافي",
  "base": "cool",
  "vertical_tag": "retail",
  "is_preset": 1,
  "brand": "#2C6FB0",
  "brand_deep": "#1E4E80",
  "accent": "#5BA3E0",
  "accent_deep": "#3E7AB5",
  "tokens_json": "{\"--canvas\": \"#F3F6F9\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#E9EEF3\", \"--surface-3\": \"#DCE4EC\", \"--ink\": \"#15191F\", \"--ink-muted\": \"#5C636E\", \"--ink-faint\": \"#93999F\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#2C6FB0\", \"--brand-deep\": \"#1E4E80\", \"--accent\": \"#5BA3E0\", \"--accent-deep\": \"#3E7AB5\", \"--brand-tint\": \"color-mix(in srgb, #2C6FB0 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #5BA3E0 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "rose-gold",
  "theme_name": "Rose Gold",
  "theme_name_ar": "الذهبي الوردي",
  "base": "pure",
  "vertical_tag": "cafe",
  "is_preset": 1,
  "brand": "#C25A78",
  "brand_deep": "#94405A",
  "accent": "#C99A5B",
  "accent_deep": "#9C7440",
  "tokens_json": "{\"--canvas\": \"#F7F7F8\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFEFF1\", \"--surface-3\": \"#E3E3E6\", \"--ink\": \"#18181B\", \"--ink-muted\": \"#5C5C61\", \"--ink-faint\": \"#9A9AA0\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.14)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#C25A78\", \"--brand-deep\": \"#94405A\", \"--accent\": \"#C99A5B\", \"--accent-deep\": \"#9C7440\", \"--brand-tint\": \"color-mix(in srgb, #C25A78 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #C99A5B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "forest",
  "theme_name": "Forest",
  "theme_name_ar": "الغابة",
  "base": "warm",
  "vertical_tag": "supermarket",
  "is_preset": 1,
  "brand": "#2E7D44",
  "brand_deep": "#1E5A30",
  "accent": "#9BB83F",
  "accent_deep": "#74902C",
  "tokens_json": "{\"--canvas\": \"#F6F4EF\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFECE4\", \"--surface-3\": \"#E7E2D7\", \"--ink\": \"#1C1A17\", \"--ink-muted\": \"#6B6760\", \"--ink-faint\": \"#9A958C\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#2E7D44\", \"--brand-deep\": \"#1E5A30\", \"--accent\": \"#9BB83F\", \"--accent-deep\": \"#74902C\", \"--brand-tint\": \"color-mix(in srgb, #2E7D44 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #9BB83F 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "sunset",
  "theme_name": "Sunset",
  "theme_name_ar": "الغروب",
  "base": "warm",
  "vertical_tag": "cafe",
  "is_preset": 1,
  "brand": "#E0682B",
  "brand_deep": "#B04A18",
  "accent": "#C03B6E",
  "accent_deep": "#922C53",
  "tokens_json": "{\"--canvas\": \"#F6F4EF\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFECE4\", \"--surface-3\": \"#E7E2D7\", \"--ink\": \"#1C1A17\", \"--ink-muted\": \"#6B6760\", \"--ink-faint\": \"#9A958C\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#E0682B\", \"--brand-deep\": \"#B04A18\", \"--accent\": \"#C03B6E\", \"--accent-deep\": \"#922C53\", \"--brand-tint\": \"color-mix(in srgb, #E0682B 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #C03B6E 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "pharma-blue",
  "theme_name": "Pharma Blue",
  "theme_name_ar": "أزرق صيدلي",
  "base": "pure",
  "vertical_tag": "pharmacy",
  "is_preset": 1,
  "brand": "#1E8CA8",
  "brand_deep": "#136277",
  "accent": "#34B27B",
  "accent_deep": "#268559",
  "tokens_json": "{\"--canvas\": \"#F7F7F8\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFEFF1\", \"--surface-3\": \"#E3E3E6\", \"--ink\": \"#18181B\", \"--ink-muted\": \"#5C5C61\", \"--ink-faint\": \"#9A9AA0\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.14)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#1E8CA8\", \"--brand-deep\": \"#136277\", \"--accent\": \"#34B27B\", \"--accent-deep\": \"#268559\", \"--brand-tint\": \"color-mix(in srgb, #1E8CA8 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #34B27B 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "hotel-noir",
  "theme_name": "Hotel Noir",
  "theme_name_ar": "الفخامة السوداء",
  "base": "dark",
  "vertical_tag": "hotel",
  "is_preset": 1,
  "brand": "#C9A24B",
  "brand_deep": "#A07E2E",
  "accent": "#D9BC72",
  "accent_deep": "#B0944A",
  "tokens_json": "{\"--canvas\": \"#15161A\", \"--surface\": \"#1E2027\", \"--surface-2\": \"#262932\", \"--surface-3\": \"#31343F\", \"--ink\": \"#F1F0ED\", \"--ink-muted\": \"#A6A49E\", \"--ink-faint\": \"#6C6A66\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#C9A24B\", \"--brand-deep\": \"#A07E2E\", \"--accent\": \"#D9BC72\", \"--accent-deep\": \"#B0944A\", \"--brand-tint\": \"color-mix(in srgb, #C9A24B 12%, #1E2027)\", \"--accent-tint\": \"color-mix(in srgb, #D9BC72 16%, #1E2027)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "market-fresh",
  "theme_name": "Market Fresh",
  "theme_name_ar": "السوق الطازج",
  "base": "pure",
  "vertical_tag": "supermarket",
  "is_preset": 1,
  "brand": "#2FA34B",
  "brand_deep": "#1E7A36",
  "accent": "#F08C1E",
  "accent_deep": "#C06E14",
  "tokens_json": "{\"--canvas\": \"#F7F7F8\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFEFF1\", \"--surface-3\": \"#E3E3E6\", \"--ink\": \"#18181B\", \"--ink-muted\": \"#5C5C61\", \"--ink-faint\": \"#9A9AA0\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.14)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#2FA34B\", \"--brand-deep\": \"#1E7A36\", \"--accent\": \"#F08C1E\", \"--accent-deep\": \"#C06E14\", \"--brand-tint\": \"color-mix(in srgb, #2FA34B 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #F08C1E 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "cafeteria-warm",
  "theme_name": "Cafeteria Warm",
  "theme_name_ar": "الكافتيريا الدافئة",
  "base": "warm",
  "vertical_tag": "cafeteria",
  "is_preset": 1,
  "brand": "#C8772E",
  "brand_deep": "#9A591C",
  "accent": "#7A9E4A",
  "accent_deep": "#5C7A34",
  "tokens_json": "{\"--canvas\": \"#F6F4EF\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFECE4\", \"--surface-3\": \"#E7E2D7\", \"--ink\": \"#1C1A17\", \"--ink-muted\": \"#6B6760\", \"--ink-faint\": \"#9A958C\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.15)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#C8772E\", \"--brand-deep\": \"#9A591C\", \"--accent\": \"#7A9E4A\", \"--accent-deep\": \"#5C7A34\", \"--brand-tint\": \"color-mix(in srgb, #C8772E 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #7A9E4A 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "mono-light",
  "theme_name": "Mono Light",
  "theme_name_ar": "أحادي فاتح",
  "base": "pure",
  "vertical_tag": "retail",
  "is_preset": 1,
  "brand": "#18181B",
  "brand_deep": "#000000",
  "accent": "#2C6FB0",
  "accent_deep": "#1E4E80",
  "tokens_json": "{\"--canvas\": \"#F7F7F8\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFEFF1\", \"--surface-3\": \"#E3E3E6\", \"--ink\": \"#18181B\", \"--ink-muted\": \"#5C5C61\", \"--ink-faint\": \"#9A9AA0\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.14)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#18181B\", \"--brand-deep\": \"#000000\", \"--accent\": \"#2C6FB0\", \"--accent-deep\": \"#1E4E80\", \"--brand-tint\": \"color-mix(in srgb, #18181B 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #2C6FB0 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "mono-dark",
  "theme_name": "Mono Dark",
  "theme_name_ar": "أحادي داكن",
  "base": "dark",
  "vertical_tag": "retail",
  "is_preset": 1,
  "brand": "#F1F0ED",
  "brand_deep": "#FFFFFF",
  "accent": "#5BA3E0",
  "accent_deep": "#3E7AB5",
  "tokens_json": "{\"--canvas\": \"#15161A\", \"--surface\": \"#1E2027\", \"--surface-2\": \"#262932\", \"--surface-3\": \"#31343F\", \"--ink\": \"#F1F0ED\", \"--ink-muted\": \"#A6A49E\", \"--ink-faint\": \"#6C6A66\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#F1F0ED\", \"--brand-deep\": \"#FFFFFF\", \"--accent\": \"#5BA3E0\", \"--accent-deep\": \"#3E7AB5\", \"--brand-tint\": \"color-mix(in srgb, #F1F0ED 12%, #1E2027)\", \"--accent-tint\": \"color-mix(in srgb, #5BA3E0 16%, #1E2027)\", \"--brand-contrast\": \"#15161A\"}"
 },
 {
  "theme_id": "saudi-green",
  "theme_name": "Saudi Green",
  "theme_name_ar": "الأخضر السعودي",
  "base": "pure",
  "vertical_tag": "national",
  "is_preset": 1,
  "brand": "#1B8A3A",
  "brand_deep": "#125E27",
  "accent": "#1B8A3A",
  "accent_deep": "#125E27",
  "tokens_json": "{\"--canvas\": \"#F7F7F8\", \"--surface\": \"#FFFFFF\", \"--surface-2\": \"#EFEFF1\", \"--surface-3\": \"#E3E3E6\", \"--ink\": \"#18181B\", \"--ink-muted\": \"#5C5C61\", \"--ink-faint\": \"#9A9AA0\", \"--border\": \"rgba(0,0,0,.08)\", \"--border-strong\": \"rgba(0,0,0,.14)\", \"--pos\": \"#0F6E56\", \"--warn\": \"#9A6212\", \"--neg\": \"#B23B3B\", \"--neg-tint\": \"#F7E9E8\", \"--brand\": \"#1B8A3A\", \"--brand-deep\": \"#125E27\", \"--accent\": \"#1B8A3A\", \"--accent-deep\": \"#125E27\", \"--brand-tint\": \"color-mix(in srgb, #1B8A3A 12%, #FFFFFF)\", \"--accent-tint\": \"color-mix(in srgb, #1B8A3A 16%, #FFFFFF)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "emerald-luxe",
  "theme_name": "Emerald Luxe",
  "theme_name_ar": "الزمرد الفاخر",
  "base": "dark",
  "vertical_tag": "hotel",
  "is_preset": 1,
  "brand": "#1FA971",
  "brand_deep": "#157750",
  "accent": "#C9A24B",
  "accent_deep": "#A07E2E",
  "tokens_json": "{\"--canvas\": \"#15161A\", \"--surface\": \"#1E2027\", \"--surface-2\": \"#262932\", \"--surface-3\": \"#31343F\", \"--ink\": \"#F1F0ED\", \"--ink-muted\": \"#A6A49E\", \"--ink-faint\": \"#6C6A66\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#1FA971\", \"--brand-deep\": \"#157750\", \"--accent\": \"#C9A24B\", \"--accent-deep\": \"#A07E2E\", \"--brand-tint\": \"color-mix(in srgb, #1FA971 12%, #1E2027)\", \"--accent-tint\": \"color-mix(in srgb, #C9A24B 16%, #1E2027)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "midnight-mint",
  "theme_name": "Midnight Mint",
  "theme_name_ar": "نعناع منتصف الليل",
  "base": "dark",
  "vertical_tag": "cafe",
  "is_preset": 1,
  "brand": "#2BC4A0",
  "brand_deep": "#1E8C72",
  "accent": "#7B8CF0",
  "accent_deep": "#5566C8",
  "tokens_json": "{\"--canvas\": \"#15161A\", \"--surface\": \"#1E2027\", \"--surface-2\": \"#262932\", \"--surface-3\": \"#31343F\", \"--ink\": \"#F1F0ED\", \"--ink-muted\": \"#A6A49E\", \"--ink-faint\": \"#6C6A66\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#2BC4A0\", \"--brand-deep\": \"#1E8C72\", \"--accent\": \"#7B8CF0\", \"--accent-deep\": \"#5566C8\", \"--brand-tint\": \"color-mix(in srgb, #2BC4A0 12%, #1E2027)\", \"--accent-tint\": \"color-mix(in srgb, #7B8CF0 16%, #1E2027)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "burgundy",
  "theme_name": "Burgundy",
  "theme_name_ar": "خمري",
  "base": "darkwarm",
  "vertical_tag": "restaurant",
  "is_preset": 1,
  "brand": "#9B2D4F",
  "brand_deep": "#741F3A",
  "accent": "#C8923B",
  "accent_deep": "#9A6E26",
  "tokens_json": "{\"--canvas\": \"#16120E\", \"--surface\": \"#211C16\", \"--surface-2\": \"#2A241C\", \"--surface-3\": \"#362E23\", \"--ink\": \"#F3EFE8\", \"--ink-muted\": \"#ABA499\", \"--ink-faint\": \"#6F695E\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#9B2D4F\", \"--brand-deep\": \"#741F3A\", \"--accent\": \"#C8923B\", \"--accent-deep\": \"#9A6E26\", \"--brand-tint\": \"color-mix(in srgb, #9B2D4F 12%, #211C16)\", \"--accent-tint\": \"color-mix(in srgb, #C8923B 16%, #211C16)\", \"--brand-contrast\": \"#ffffff\"}"
 },
 {
  "theme_id": "graphite-lime",
  "theme_name": "Graphite Lime",
  "theme_name_ar": "جرافيت ليموني",
  "base": "dark",
  "vertical_tag": "retail",
  "is_preset": 1,
  "brand": "#A6E22E",
  "brand_deep": "#7FB019",
  "accent": "#5BA3E0",
  "accent_deep": "#3E7AB5",
  "tokens_json": "{\"--canvas\": \"#15161A\", \"--surface\": \"#1E2027\", \"--surface-2\": \"#262932\", \"--surface-3\": \"#31343F\", \"--ink\": \"#F1F0ED\", \"--ink-muted\": \"#A6A49E\", \"--ink-faint\": \"#6C6A66\", \"--border\": \"rgba(255,255,255,.10)\", \"--border-strong\": \"rgba(255,255,255,.20)\", \"--pos\": \"#3DD9A8\", \"--warn\": \"#E0A53B\", \"--neg\": \"#E86A6A\", \"--neg-tint\": \"rgba(232,106,106,.14)\", \"--brand\": \"#A6E22E\", \"--brand-deep\": \"#7FB019\", \"--accent\": \"#5BA3E0\", \"--accent-deep\": \"#3E7AB5\", \"--brand-tint\": \"color-mix(in srgb, #A6E22E 12%, #1E2027)\", \"--accent-tint\": \"color-mix(in srgb, #5BA3E0 16%, #1E2027)\", \"--brand-contrast\": \"#15161A\"}"
 }
]

PAYMENT_MODES = [
 {
  "mode_id": "cash",
  "mode_name": "Cash",
  "mode_name_ar": "نقدًا",
  "kind": "cash",
  "icon": "💵",
  "opens_cash_drawer": 1,
  "requires_terminal": 0,
  "requires_reference": 0,
  "sort": 0
 },
 {
  "mode_id": "mada",
  "mode_name": "mada",
  "mode_name_ar": "مدى",
  "kind": "card",
  "icon": "💳",
  "opens_cash_drawer": 0,
  "requires_terminal": 1,
  "requires_reference": 0,
  "sort": 1
 },
 {
  "mode_id": "visa",
  "mode_name": "Visa / Mastercard",
  "mode_name_ar": "فيزا / ماستركارد",
  "kind": "card",
  "icon": "💳",
  "opens_cash_drawer": 0,
  "requires_terminal": 1,
  "requires_reference": 0,
  "sort": 2
 },
 {
  "mode_id": "apple_pay",
  "mode_name": "Apple Pay / mada wallet",
  "mode_name_ar": "آبل باي",
  "kind": "wallet",
  "icon": "",
  "opens_cash_drawer": 0,
  "requires_terminal": 1,
  "requires_reference": 0,
  "sort": 3
 },
 {
  "mode_id": "stc_pay",
  "mode_name": "STC Pay",
  "mode_name_ar": "إس تي سي باي",
  "kind": "wallet",
  "icon": "📲",
  "opens_cash_drawer": 0,
  "requires_terminal": 0,
  "requires_reference": 1,
  "sort": 4
 },
 {
  "mode_id": "loyalty",
  "mode_name": "Loyalty Points",
  "mode_name_ar": "نقاط الولاء",
  "kind": "loyalty",
  "icon": "⭐",
  "opens_cash_drawer": 0,
  "requires_terminal": 0,
  "requires_reference": 0,
  "sort": 5
 },
 {
  "mode_id": "gift_card",
  "mode_name": "Gift Card",
  "mode_name_ar": "بطاقة هدية",
  "kind": "voucher",
  "icon": "🎁",
  "opens_cash_drawer": 0,
  "requires_terminal": 0,
  "requires_reference": 1,
  "sort": 6
 },
 {
  "mode_id": "bank_transfer",
  "mode_name": "Bank Transfer",
  "mode_name_ar": "تحويل بنكي",
  "kind": "transfer",
  "icon": "🏦",
  "opens_cash_drawer": 0,
  "requires_terminal": 0,
  "requires_reference": 1,
  "sort": 7
 },
 {
  "mode_id": "room_charge",
  "mode_name": "Room Charge",
  "mode_name_ar": "على الغرفة",
  "kind": "room_charge",
  "icon": "🏨",
  "opens_cash_drawer": 0,
  "requires_terminal": 0,
  "requires_reference": 1,
  "sort": 8
 },
 {
  "mode_id": "meal_credit",
  "mode_name": "Meal Credit",
  "mode_name_ar": "رصيد وجبات",
  "kind": "meal_credit",
  "icon": "🍽️",
  "opens_cash_drawer": 0,
  "requires_terminal": 0,
  "requires_reference": 0,
  "sort": 9
 }
]


def after_install():
    _ensure_roles()
    _ensure_custom_fields()
    seed_themes()
    seed_payment_modes()
    seed_denominations()
    seed_branding()
    frappe.db.commit()


def after_migrate():
    _ensure_roles()
    _ensure_custom_fields()
    seed_themes()          # refresh preset themes on every migrate
    seed_payment_modes()
    seed_denominations()
    seed_branding()        # backfill primary_theme once themes exist
    frappe.db.commit()


DENOMS = [
    ("SAR 500", 500, "note"), ("SAR 200", 200, "note"), ("SAR 100", 100, "note"),
    ("SAR 50", 50, "note"), ("SAR 10", 10, "note"), ("SAR 5", 5, "note"),
    ("SAR 1", 1, "coin"), ("50 halala", 0.5, "coin"), ("25 halala", 0.25, "coin"),
    ("10 halala", 0.1, "coin"),
]


def seed_denominations():
    for i, (label, value, kind) in enumerate(DENOMS):
        if frappe.db.exists("AlphaX Currency Denomination", label):
            continue
        frappe.get_doc({"doctype": "AlphaX Currency Denomination", "label": label,
                        "currency": "SAR", "value": value, "kind": kind,
                        "enabled": 1, "sort": i}).insert(ignore_permissions=True)


def _ensure_roles():
    for role in ("AlphaX POS Manager", "AlphaX POS User"):
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role, "desk_access": 1}).insert(ignore_permissions=True)


def seed_themes():
    for t in THEMES:
        if frappe.db.exists("AlphaX Theme", t["theme_id"]):
            doc = frappe.get_doc("AlphaX Theme", t["theme_id"])
            doc.update(t)
            doc.save(ignore_permissions=True)
        else:
            d = {"doctype": "AlphaX Theme"}
            d.update(t)
            frappe.get_doc(d).insert(ignore_permissions=True)


def seed_payment_modes():
    for m in PAYMENT_MODES:
        if frappe.db.exists("AlphaX Payment Mode", m["mode_id"]):
            continue
        d = {"doctype": "AlphaX Payment Mode", "enabled": 1}
        d.update(m)
        frappe.get_doc(d).insert(ignore_permissions=True)


def seed_branding():
    """Set sane defaults on the AlphaX Branding single. Idempotent and field-wise:
    each default is only filled when empty, so the primary_theme link is set AFTER
    themes exist (never at init_singles time, which would fail link validation)."""
    b = frappe.get_single("AlphaX Branding")
    changed = False
    if not b.brand_name:
        b.brand_name = "AlphaX POS"
        b.allow_theme_switch = 1
        b.allow_theme_custom = 1
        b.enable_arabic = 1
        b.currency_symbol = "SAR"
        changed = True
    # Decoupled from brand_name: only link a theme that actually exists yet.
    if not b.primary_theme and frappe.db.exists("AlphaX Theme", "majlis-green"):
        b.primary_theme = "majlis-green"
        changed = True
    if changed:
        b.save(ignore_permissions=True)


# ── shared token builder (used by boot.upsert_custom_theme) ──────────
_BASES = {
 "warm":     dict(canvas="#F6F4EF", surface="#FFFFFF", s2="#EFECE4", s3="#E7E2D7", ink="#1C1A17", muted="#6B6760", faint="#9A958C", border="rgba(0,0,0,.08)", bs="rgba(0,0,0,.15)", pos="#0F6E56", warn="#9A6212", neg="#B23B3B", negt="#F7E9E8"),
 "cool":     dict(canvas="#F3F6F9", surface="#FFFFFF", s2="#E9EEF3", s3="#DCE4EC", ink="#15191F", muted="#5C636E", faint="#93999F", border="rgba(0,0,0,.08)", bs="rgba(0,0,0,.15)", pos="#0F6E56", warn="#9A6212", neg="#B23B3B", negt="#F7E9E8"),
 "pure":     dict(canvas="#F7F7F8", surface="#FFFFFF", s2="#EFEFF1", s3="#E3E3E6", ink="#18181B", muted="#5C5C61", faint="#9A9AA0", border="rgba(0,0,0,.08)", bs="rgba(0,0,0,.14)", pos="#0F6E56", warn="#9A6212", neg="#B23B3B", negt="#F7E9E8"),
 "dark":     dict(canvas="#15161A", surface="#1E2027", s2="#262932", s3="#31343F", ink="#F1F0ED", muted="#A6A49E", faint="#6C6A66", border="rgba(255,255,255,.10)", bs="rgba(255,255,255,.20)", pos="#3DD9A8", warn="#E0A53B", neg="#E86A6A", negt="rgba(232,106,106,.14)"),
 "darkwarm": dict(canvas="#16120E", surface="#211C16", s2="#2A241C", s3="#362E23", ink="#F3EFE8", muted="#ABA499", faint="#6F695E", border="rgba(255,255,255,.10)", bs="rgba(255,255,255,.20)", pos="#3DD9A8", warn="#E0A53B", neg="#E86A6A", negt="rgba(232,106,106,.14)"),
}


def _surface_for_base(base):
    return _BASES.get(base, _BASES["warm"])["surface"]


def _light_text(hexc):
    hexc = (hexc or "#000").lstrip("#")
    if len(hexc) < 6:
        return False
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) > 165


def _tokens(base, brand, brand_deep, accent, accent_deep):
    b = _BASES.get(base, _BASES["warm"])
    return {
        "--canvas": b["canvas"], "--surface": b["surface"], "--surface-2": b["s2"], "--surface-3": b["s3"],
        "--ink": b["ink"], "--ink-muted": b["muted"], "--ink-faint": b["faint"],
        "--border": b["border"], "--border-strong": b["bs"],
        "--pos": b["pos"], "--warn": b["warn"], "--neg": b["neg"], "--neg-tint": b["negt"],
        "--brand": brand, "--brand-deep": brand_deep, "--accent": accent, "--accent-deep": accent_deep,
        "--brand-tint": f"color-mix(in srgb, {brand} 12%, {b['surface']})",
        "--accent-tint": f"color-mix(in srgb, {accent} 16%, {b['surface']})",
        "--brand-contrast": "#15161A" if _light_text(brand) else "#ffffff",
    }


def _ensure_custom_fields():
    """Link a Stock Entry back to the POS order that triggered the backflush."""
    if not frappe.db.exists("Custom Field", "Stock Entry-alphax_pos_order"):
        frappe.get_doc({
            "doctype": "Custom Field", "dt": "Stock Entry",
            "fieldname": "alphax_pos_order", "label": "AlphaX POS Order",
            "fieldtype": "Data", "read_only": 1, "insert_after": "stock_entry_type",
            "unique": 1, "no_copy": 1,
        }).insert(ignore_permissions=True)
