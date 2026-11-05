def promote():
    with open('app/src/pages/events/coco-pikmin/staging.astro', 'r', encoding='utf-8') as f:
        stag_content = f.read()

    # Create prod content from stag_content:
    prod_content = stag_content

    # 1. Fix relative imports
    prod_content = prod_content.replace(
        "import BaseLayout from '../../../layouts/BaseLayout.astro';",
        "import BaseLayout from '../../layouts/BaseLayout.astro';"
    )
    prod_content = prod_content.replace(
        "import stores from '../../../data/coco_stores_staging.json';",
        "import stores from '../../data/coco_stores.json';"
    )

    # 2. Fix title
    prod_content = prod_content.replace(
        "title={`[Staging 測試版] ` + title}",
        "title={title}"
    )

    # 3. Remove staging yellow indicator banner
    staging_banner = """    <!-- Staging Environment Indicator Banner -->
    <div style="background: #FEF3C7; border-bottom: 2px solid #F59E0B; padding: 0.5rem 1rem; text-align: center; font-size: 0.875rem; font-weight: 700; color: #92400E; z-index: 50; position: relative;">
      [測試預覽環境 Staging] 此頁面用於驗證新功能，測試完畢確認無誤後將同步發布至正式版。
    </div>
"""
    if staging_banner in prod_content:
        prod_content = prod_content.replace(staging_banner, "")
    else:
        staging_banner_crlf = staging_banner.replace('\n', '\r\n')
        if staging_banner_crlf in prod_content:
            prod_content = prod_content.replace(staging_banner_crlf, "")

    with open('app/src/pages/events/coco-pikmin.astro', 'w', encoding='utf-8') as f:
        f.write(prod_content)
    print("app/src/pages/events/coco-pikmin.astro successfully updated for Production!")

if __name__ == '__main__':
    promote()
