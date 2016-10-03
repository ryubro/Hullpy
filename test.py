from hull import Hull
import config_for_test as config

hull = Hull(platform_id=config.platform_id,
            org_url=config.org_url)
admin_hull = Hull(platform_id=config.platform_id,
                  org_url=config.org_url,
                  platform_secret=config.platform_secret)
test_user = config.test_user_id

try:
    print hull.get(test_user)

    print admin_hull.put(test_user, {"extra": {"test_hullpy": "test"}})

    print admin_hull.put(test_user, {"extra": {"test_hullpy": "overridden"}})

    print admin_hull.put(test_user, {"extra": {"test_hullpy": None}})
except:
    raise
