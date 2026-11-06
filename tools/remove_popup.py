import re

for path in ['app/src/pages/events/coco-pikmin.astro', 'app/src/pages/events/coco-pikmin/staging.astro']:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Clean any remnant of float toast or button
    c = re.sub(r'\s*<button type="button" class="btn-float-reload".*?</div>\s*</div>', '', c, flags=re.DOTALL)
    c = re.sub(r'\s*<div id="live-update-float-toast".*?</div>\s*</div>', '', c, flags=re.DOTALL)

    # Clean CSS of live-update-float-toast
    c = re.sub(r'/\* Global Unscoped Styles for Live Update Floating Toast \*/.*?</style>', '</style>', c, flags=re.DOTALL)
    c = re.sub(r'/\* Live Update Floating Prompt.*?@keyframes icon-bounce.*?\n\s*\}', '', c, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

print('Cleaned both files cleanly.')
