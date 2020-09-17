insert_film = '''
INSERT INTO films (provider_id, title, date, synopsis, note_press, note_people) 
VALUES (%s, %s, %s, %s, %s, %s);
'''


save_scraped_page = '''
TRUNCATE scrap_progress;
INSERT INTO scrap_progress (page_id) VALUES (%s);
'''
get_last_scraped_page = "SELECT page_id FROM scrap_progress;"

insert_genre = '''
SELECT * FROM genres
WHERE name = %s;
IF NOT found THEN
    INSERT INTO genres (name)
    VALUES (%s);
END IF;
'''