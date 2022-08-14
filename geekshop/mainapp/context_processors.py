def menu_links(request):
    print(f'context processor basket works')
    return {
        "menu_links": [
            {"url": "main", "active": ["main"], "name": "домой"},
            {
                "url": "products:all",
                "active": ["products:all", "products:category"],
                "name": "продукты",
            },
            {"url": "contact", "active": ["contact"], "name": "контакты"},
        ]
    }


