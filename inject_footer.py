import sys
import os

footer_path = r'C:\Users\ADITHYAN\.gemini\antigravity-ide\brain\ad67dd81-9167-4734-b024-b96466a9b7b0\scratch\footer.html'
with open(footer_path, 'r', encoding='utf-8') as f:
    footer_html = f.read()

target = 'restaurant.html'
with open(target, 'r', encoding='utf-8') as f:
    content = f.read()

marker = '<!-- Exact Swiggy Menu FAB & View Cart Footer Container -->'

if marker in content:
    if '<div class="restaurant-footer-sections">' not in content:
        content = content.replace(marker, footer_html + '\n\n  ' + marker)
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Footer injected successfully.")
    else:
        print("Footer already injected.")
else:
    print("Marker not found in restaurant.html!")
