from scraper import check_updates

if __name__ == "__main__":
    new_updates = check_updates()
    if new_updates:
        print("Updates found:")
        for site, data in new_updates["sites"].items():
            print(f"- {site}: {data[0]} ")
    else:
        print("No new updates.")