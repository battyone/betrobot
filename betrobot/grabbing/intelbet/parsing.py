import bs4
import re


def get_text(tag_or_string):
  if isinstance(tag_or_string, bs4.Tag):
    return tag_or_string.get_text(separator=' ', strip=True)
  else:
    return str(tag_or_string)


def handle_date(html_or_file):
    data = []

    soup = bs4.BeautifulSoup(html_or_file, 'lxml')

    tables = soup.find_all('table', class_='meeting-odds')
    for table in tables:
      country_and_tournament_th = table.find('th', class_='tournament-name', recursive=True)
      links = country_and_tournament_th.find_all('a', recursive=True)
      if len(links) > 1:
          intelbet_country = get_text(links[0])
          intelbet_tournament = get_text(links[1])
      else:
          intelbet_country = None
          intelbet_tournament = get_text(links[0])

      trs = table.find('tbody').find_all('tr', recursive=False)
      for tr in trs:
          teams_tags = tr.find('td', class_='name-with-icon', recursive=False).find('a', recursive=False).find('span', recursive=False).find_all('span', recursive=False)
          intelbet_home = get_text(teams_tags[0])
          intelbet_away = get_text(teams_tags[2])

          url_tag = tr.find('td', class_='name-with-icon', recursive=False).find('a', recursive=False)
          url = 'http:%s' % (url_tag['href'],)

          match_time_tag = tr.find('td', class_='tiles-bet-time', recursive=False)
          match_time_str = get_text(match_time_tag)

          item = (intelbet_country, intelbet_tournament, intelbet_home, intelbet_away, url, match_time_str)
          data.append(item)

    return data


def _extract_player_names(table_tag):
    player_names = []

    trs = table_tag.find('tbody').find_all('tr', recursive=False)
    for tr in trs:
        tds = tr.find_all('td', recursive=False)
        player_name_td = tds[1]
        player_name = get_text(player_name_td)
        player_names.append(player_name)

    return player_names


def handle_match(html_or_file):
    home_player_names = None
    away_player_names = None

    soup = bs4.BeautifulSoup(html_or_file, 'lxml')

    match_team_tables = soup.find_all('table', class_='match-team-table')

    home_lineup_table_tag = match_team_tables[4]
    home_player_names = _extract_player_names(home_lineup_table_tag)

    away_lineup_table_tag = match_team_tables[5]
    away_player_names = _extract_player_names(away_lineup_table_tag)

    # TODO: Парсить и другие таблицы составов
    # Учитывать фразы типа "Травма ноги"

    return (home_player_names, away_player_names)
