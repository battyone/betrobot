from betrobot.util.sport_util import bet_satisfy, count_events_of_teams, is_home_or_away_by_betcity_team_name, is_goal, is_corner, is_yellow_card, is_first_period, is_second_period


def _check_goals_result_1(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    ground_truth = goals_home_count > goals_away_count

    return ground_truth


def _check_goals_result_2(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    ground_truth = goals_home_count < goals_away_count

    return ground_truth


def _check_goals_result_1X(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    ground_truth = goals_home_count >= goals_away_count

    return ground_truth


def _check_goals_result_X2(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    ground_truth = goals_home_count <= goals_away_count

    return ground_truth


def _check_goals_first_period_result_1(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    ground_truth = goals_home_count > goals_away_count

    return ground_truth


def _check_goals_first_period_result_2(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    ground_truth = goals_home_count < goals_away_count

    return ground_truth


def _check_goals_first_period_result_1X(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    ground_truth = goals_home_count >= goals_away_count

    return ground_truth


def _check_goals_first_period_result_X2(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    ground_truth = goals_home_count <= goals_away_count

    return ground_truth


def _check_goals_second_period_result_1(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    ground_truth = goals_home_count > goals_away_count

    return ground_truth


def _check_goals_second_period_result_2(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    ground_truth = goals_home_count < goals_away_count

    return ground_truth


def _check_goals_second_period_result_1X(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    ground_truth = goals_home_count >= goals_away_count

    return ground_truth


def _check_goals_second_period_result_X2(bet, match_special_word, whoscored_match):
    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    ground_truth = goals_home_count <= goals_away_count

    return ground_truth


def _check_goals_handicap(bet, match_special_word, whoscored_match):
    team = bet[2]
    handicap = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count + handicap > goals_away_count
    elif is_home_or_away == 'A':
        ground_truth = goals_home_count < goals_away_count + handicap
    else:
        return None

    return ground_truth


def _check_goals_first_period_handicap(bet, match_special_word, whoscored_match):
    team = bet[3]
    handicap = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count + handicap > goals_away_count
    elif is_home_or_away == 'A':
        ground_truth = goals_home_count < goals_away_count + handicap
    else:
        return None

    return ground_truth


def _check_goals_second_period_handicap(bet, match_special_word, whoscored_match):
    team = bet[3]
    handicap = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count + handicap > goals_away_count
    elif is_home_or_away == 'A':
        ground_truth = goals_home_count < goals_away_count + handicap
    else:
        return None

    return ground_truth


def _check_goals_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    goals_count = goals_home_count + goals_away_count
    ground_truth = goals_count > total

    return ground_truth


def _check_goals_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(is_goal, whoscored_match)
    goals_count = goals_home_count + goals_away_count
    ground_truth = goals_count < total

    return ground_truth


def _check_goals_first_period_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    goals_count = goals_home_count + goals_away_count
    ground_truth = goals_count > total

    return ground_truth


def _check_goals_first_period_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    goals_count = goals_home_count + goals_away_count
    ground_truth = goals_count < total

    return ground_truth


def _check_goals_second_period_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    goals_count = goals_home_count + goals_away_count
    ground_truth = goals_count > total

    return ground_truth


def _check_goals_second_period_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    goals_count = goals_home_count + goals_away_count
    ground_truth = goals_count < total
    return ground_truth


def _check_goals_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = goals_away_count > total
    else:
        return None

    return ground_truth


def _check_goals_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = goals_away_count < total
    else:
        return None

    return ground_truth


def _check_goals_first_period_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = goals_away_count > total
    else:
        return None

    return ground_truth


def _check_goals_first_period_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = goals_away_count < total
    else:
        return None

    return ground_truth


def _check_goals_second_period_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = goals_away_count > total
    else:
        return None

    return ground_truth


def _check_goals_second_period_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (goals_home_count, goals_away_count) = count_events_of_teams(lambda event: is_goal(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = goals_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = goals_away_count < total
    else:
        return None

    return ground_truth




def _check_corners_result_1(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    ground_truth = corners_home_count > corners_away_count

    return ground_truth


def _check_corners_result_1X(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    ground_truth = corners_home_count >= corners_away_count

    return ground_truth


def _check_corners_result_X2(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    ground_truth = corners_home_count <= corners_away_count

    return ground_truth


def _check_corners_result_2(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    ground_truth = corners_home_count < corners_away_count

    return ground_truth


def _check_corners_first_period_result_1(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    ground_truth = corners_home_count > corners_away_count

    return ground_truth


def _check_corners_first_period_result_1X(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    ground_truth = corners_home_count >= corners_away_count

    return ground_truth


def _check_corners_first_period_result_X2(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    ground_truth = corners_home_count <= corners_away_count

    return ground_truth


def _check_corners_first_period_result_2(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    ground_truth = corners_home_count < corners_away_count

    return ground_truth


def _check_corners_second_period_result_1(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    ground_truth = corners_home_count > corners_away_count

    return ground_truth


def _check_corners_second_period_result_1X(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    ground_truth = corners_home_count >= corners_away_count

    return ground_truth


def _check_corners_second_period_result_X2(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    ground_truth = corners_home_count <= corners_away_count

    return ground_truth


def _check_corners_second_period_result_2(bet, match_special_word, whoscored_match):
    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    ground_truth = corners_home_count < corners_away_count

    return ground_truth


def _check_corners_handicap(bet, match_special_word, whoscored_match):
    team = bet[2]
    handicap = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count + handicap > corners_away_count
    elif is_home_or_away == 'A':
        ground_truth = corners_home_count < corners_away_count + handicap
    else:
        return None

    return ground_truth


def _check_corners_first_period_handicap(bet, match_special_word, whoscored_match):
    team = bet[3]
    handicap = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count + handicap > corners_away_count
    elif is_home_or_away == 'A':
        ground_truth = corners_home_count < corners_away_count + handicap
    else:
        return None

    return ground_truth


def _check_corners_second_period_handicap(bet, match_special_word, whoscored_match):
    team = bet[3]
    handicap = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count + handicap > corners_away_count
    elif is_home_or_away == 'A':
        ground_truth = corners_home_count < corners_away_count + handicap
    else:
        return None

    return ground_truth


def _check_corners_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    corners_count = corners_home_count + corners_away_count
    ground_truth = corners_count > total

    return ground_truth


def _check_corners_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(is_corner, whoscored_match)
    corners_count = corners_home_count + corners_away_count
    ground_truth = corners_count < total

    return ground_truth


def _check_corners_first_period_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    corners_count = corners_home_count + corners_away_count
    ground_truth = corners_count > total

    return ground_truth


def _check_corners_first_period_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    corners_count = corners_home_count + corners_away_count
    ground_truth = corners_count < total

    return ground_truth


def _check_corners_second_period_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    corners_count = corners_home_count + corners_away_count
    ground_truth = corners_count > total

    return ground_truth


def _check_corners_second_period_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    corners_count = corners_home_count + corners_away_count
    ground_truth = corners_count < total
    return ground_truth


def _check_corners_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = corners_away_count > total
    else:
        return None

    return ground_truth


def _check_corners_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = corners_away_count < total
    else:
        return None

    return ground_truth


def _check_corners_first_period_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = corners_away_count > total
    else:
        return None

    return ground_truth


def _check_corners_first_period_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = corners_away_count < total
    else:
        return None

    return ground_truth


def _check_corners_second_period_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = corners_away_count > total
    else:
        return None

    return ground_truth


def _check_corners_second_period_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (corners_home_count, corners_away_count) = count_events_of_teams(lambda event: is_corner(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = corners_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = corners_away_count < total
    else:
        return None

    return ground_truth




def _check_yellow_cards_result_1(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    ground_truth = yellow_cards_home_count > yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_result_1X(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    ground_truth = yellow_cards_home_count >= yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_result_X2(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    ground_truth = yellow_cards_home_count <= yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_result_2(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    ground_truth = yellow_cards_home_count < yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_first_period_result_1(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count > yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_first_period_result_1X(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count >= yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_first_period_result_X2(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count <= yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_first_period_result_2(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count < yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_second_period_result_1(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count > yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_second_period_result_1X(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count >= yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_second_period_result_X2(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count <= yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_second_period_result_2(bet, match_special_word, whoscored_match):
    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    ground_truth = yellow_cards_home_count < yellow_cards_away_count

    return ground_truth


def _check_yellow_cards_handicap(bet, match_special_word, whoscored_match):
    team = bet[2]
    handicap = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count + handicap > yellow_cards_away_count
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_home_count < yellow_cards_away_count + handicap
    else:
        return None

    return ground_truth


def _check_yellow_cards_first_period_handicap(bet, match_special_word, whoscored_match):
    team = bet[3]
    handicap = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count + handicap > yellow_cards_away_count
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_home_count < yellow_cards_away_count + handicap
    else:
        return None

    return ground_truth


def _check_yellow_cards_second_period_handicap(bet, match_special_word, whoscored_match):
    team = bet[3]
    handicap = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count + handicap > yellow_cards_away_count
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_home_count < yellow_cards_away_count + handicap
    else:
        return None

    return ground_truth


def _check_yellow_cards_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    yellow_cards_count = yellow_cards_home_count + yellow_cards_away_count
    ground_truth = yellow_cards_count > total

    return ground_truth


def _check_yellow_cards_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(is_yellow_card, whoscored_match)
    yellow_cards_count = yellow_cards_home_count + yellow_cards_away_count
    ground_truth = yellow_cards_count < total

    return ground_truth


def _check_yellow_cards_first_period_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    yellow_cards_count = yellow_cards_home_count + yellow_cards_away_count
    ground_truth = yellow_cards_count > total

    return ground_truth


def _check_yellow_cards_first_period_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    yellow_cards_count = yellow_cards_home_count + yellow_cards_away_count
    ground_truth = yellow_cards_count < total

    return ground_truth


def _check_yellow_cards_second_period_total_greater(bet, match_special_word, whoscored_match):
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    yellow_cards_count = yellow_cards_home_count + yellow_cards_away_count
    ground_truth = yellow_cards_count > total

    return ground_truth


def _check_yellow_cards_second_period_total_lesser(bet, match_special_word, whoscored_match):
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    yellow_cards_count = yellow_cards_home_count + yellow_cards_away_count
    ground_truth = yellow_cards_count < total
    return ground_truth


def _check_yellow_cards_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_away_count > total
    else:
        return None

    return ground_truth


def _check_yellow_cards_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_away_count < total
    else:
        return None

    return ground_truth


def _check_yellow_cards_first_period_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_away_count > total
    else:
        return None

    return ground_truth


def _check_yellow_cards_first_period_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_first_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_away_count < total
    else:
        return None

    return ground_truth


def _check_yellow_cards_second_period_individual_total_greater(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count > total
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_away_count > total
    else:
        return None

    return ground_truth


def _check_yellow_cards_second_period_individual_total_lesser(bet, match_special_word, whoscored_match):
    team = bet[2]
    total = bet[4]

    (yellow_cards_home_count, yellow_cards_away_count) = count_events_of_teams(lambda event: is_yellow_card(event) and is_second_period(event), whoscored_match)
    is_home_or_away = is_home_or_away_by_betcity_team_name(team, whoscored_match)
    if is_home_or_away == 'H':
        ground_truth = yellow_cards_home_count < total
    elif is_home_or_away == 'A':
        ground_truth = yellow_cards_away_count < total
    else:
        return None

    return ground_truth




def check_bet(bet, match_special_word, whoscored_match):
    if bet is None or whoscored_match is None:
        return None

    rules = [
        [ None, (None, 'Исход', '', '1', None), _check_goals_result_1 ],
        [ None, (None, 'Исход', '', '1X', None), _check_goals_result_1X ],
        [ None, (None, 'Исход', '', 'X2', None), _check_goals_result_X2 ],
        [ None, (None, 'Исход', '', '2', None), _check_goals_result_2 ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', '', '1', None), _check_goals_first_period_result_1 ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', '', '1X', None), _check_goals_first_period_result_1X ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', '', 'X2', None), _check_goals_first_period_result_X2 ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', '', '2', None), _check_goals_first_period_result_2 ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', '', '1', None), _check_goals_second_period_result_1 ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', '', '1X', None), _check_goals_second_period_result_1X ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', '', 'X2', None), _check_goals_second_period_result_X2 ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', '', '2', None), _check_goals_second_period_result_2 ],
        [ None, (None, 'Фора', '*', '', '*'), _check_goals_handicap ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', 'Фора', '*', '*'), _check_goals_first_period_handicap ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', 'Фора', '*', '*'), _check_goals_second_period_handicap ],
        [ None, (None, 'Тотал', '', 'Бол', '*'), _check_goals_total_greater ],
        [ None, (None, 'Дополнительные тоталы', '', 'Бол', '*'), _check_goals_total_greater ],
        [ None, (None, 'Тотал', '', 'Мен', '*'), _check_goals_total_lesser ],
        [ None, (None, 'Дополнительные тоталы', '', 'Мен', '*'), _check_goals_total_lesser ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', '', 'Бол', '*'), _check_goals_first_period_total_greater ],
        [ None, (None, 'Исходы по таймам (1-й тайм)', '', 'Мен', '*'), _check_goals_first_period_total_lesser ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', '', 'Бол', '*'), _check_goals_second_period_total_greater ],
        [ None, (None, 'Исходы по таймам (2-й тайм)', '', 'Мен', '*'), _check_goals_second_period_total_lesser ],
        [ None, (None, 'Индивидуальный тотал', '*', 'Бол', '*'), _check_goals_individual_total_greater ],
        [ None, (None, 'Индивидуальный тотал', '*', 'Мен', '*'), _check_goals_individual_total_lesser ],
        [ None, (None, 'Индивидуальный тотал 1-й тайм', '*', 'Бол', '*'), _check_goals_first_period_individual_total_greater ],
        [ None, (None, 'Индивидуальный тотал 1-й тайм', '*', 'Мен', '*'), _check_goals_first_period_individual_total_lesser ],
        [ None, (None, 'Индивидуальный тотал 2-й тайм', '*', 'Бол', '*'), _check_goals_second_period_individual_total_greater ],
        [ None, (None, 'Индивидуальный тотал 2-й тайм', '*', 'Мен', '*'), _check_goals_second_period_individual_total_lesser ],

        [ 'УГЛ', ('УГЛ', 'Исход', '', '1', None), _check_corners_result_1 ],
        [ 'УГЛ', ('УГЛ', 'Исход', '', '1X', None), _check_corners_result_1X ],
        [ 'УГЛ', ('УГЛ', 'Исход', '', 'X2', None), _check_corners_result_X2 ],
        [ 'УГЛ', ('УГЛ', 'Исход', '', '2', None), _check_corners_result_2 ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', '', '1', None), _check_corners_first_period_result_1 ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', '', '1X', None), _check_corners_first_period_result_1X ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', '', 'X2', None), _check_corners_first_period_result_X2 ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', '', '2', None), _check_corners_first_period_result_2 ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', '', '1', None), _check_corners_second_period_result_1 ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', '', '1X', None), _check_corners_second_period_result_1X ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', '', 'X2', None), _check_corners_second_period_result_X2 ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', '', '2', None), _check_corners_second_period_result_2 ],
        [ 'УГЛ', ('УГЛ', 'Фора', '*', '', '*'), _check_corners_handicap ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', 'Фора', '*', '*'), _check_corners_first_period_handicap ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', 'Фора', '*', '*'), _check_corners_second_period_handicap ],
        [ 'УГЛ', ('УГЛ', 'Тотал', '', 'Бол', '*'), _check_corners_total_greater ],
        [ 'УГЛ', ('УГЛ', 'Дополнительные тоталы', '', 'Бол', '*'), _check_corners_total_greater ],
        [ 'УГЛ', ('УГЛ', 'Тотал', '', 'Мен', '*'), _check_corners_total_lesser ],
        [ 'УГЛ', ('УГЛ', 'Дополнительные тоталы', '', 'Мен', '*'), _check_corners_total_lesser ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', '', 'Бол', '*'), _check_corners_first_period_total_greater ],
        [ 'УГЛ', (None, 'Исходы по таймам (1-й тайм)', '', 'Мен', '*'), _check_corners_first_period_total_lesser ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', '', 'Бол', '*'), _check_corners_second_period_total_greater ],
        [ 'УГЛ', (None, 'Исходы по таймам (2-й тайм)', '', 'Мен', '*'), _check_corners_second_period_total_lesser ],
        [ 'УГЛ', ('УГЛ', 'Индивидуальный тотал', '*', 'Бол', '*'), _check_corners_individual_total_greater ],
        [ 'УГЛ', ('УГЛ', 'Индивидуальный тотал', '*', 'Мен', '*'), _check_corners_individual_total_lesser ],
        [ 'УГЛ', ('УГЛ', 'Индивидуальный тотал 1-й тайм', '*', 'Бол', '*'), _check_corners_first_period_individual_total_greater ],
        [ 'УГЛ', ('УГЛ', 'Индивидуальный тотал 1-й тайм', '*', 'Мен', '*'), _check_corners_first_period_individual_total_lesser ],
        [ 'УГЛ', ('УГЛ', 'Индивидуальный тотал 2-й тайм', '*', 'Бол', '*'), _check_corners_second_period_individual_total_greater ],
        [ 'УГЛ', ('УГЛ', 'Индивидуальный тотал 2-й тайм', '*', 'Мен', '*'), _check_corners_second_period_individual_total_lesser ],

        [ 'ЖК', ('ЖК', 'Исход', '', '1', None), _check_yellow_cards_result_1 ],
        [ 'ЖК', ('ЖК', 'Исход', '', '1X', None), _check_yellow_cards_result_1X ],
        [ 'ЖК', ('ЖК', 'Исход', '', 'X2', None), _check_yellow_cards_result_X2 ],
        [ 'ЖК', ('ЖК', 'Исход', '', '2', None), _check_yellow_cards_result_2 ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', '', '1', None), _check_yellow_cards_first_period_result_1 ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', '', '1X', None), _check_yellow_cards_first_period_result_1X ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', '', 'X2', None), _check_yellow_cards_first_period_result_X2 ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', '', '2', None), _check_yellow_cards_first_period_result_2 ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', '', '1', None), _check_yellow_cards_second_period_result_1 ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', '', '1X', None), _check_yellow_cards_second_period_result_1X ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', '', 'X2', None), _check_yellow_cards_second_period_result_X2 ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', '', '2', None), _check_yellow_cards_second_period_result_2 ],
        [ 'ЖК', ('ЖК', 'Фора', '*', '', '*'), _check_yellow_cards_handicap ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', 'Фора', '*', '*'), _check_yellow_cards_first_period_handicap ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', 'Фора', '*', '*'), _check_yellow_cards_second_period_handicap ],
        [ 'ЖК', ('ЖК', 'Тотал', '', 'Бол', '*'), _check_yellow_cards_total_greater ],
        [ 'ЖК', ('ЖК', 'Дополнительные тоталы', '', 'Бол', '*'), _check_yellow_cards_total_greater ],
        [ 'ЖК', ('ЖК', 'Тотал', '', 'Мен', '*'), _check_yellow_cards_total_lesser ],
        [ 'ЖК', ('ЖК', 'Дополнительные тоталы', '', 'Мен', '*'), _check_yellow_cards_total_lesser ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', '', 'Бол', '*'), _check_yellow_cards_first_period_total_greater ],
        [ 'ЖК', (None, 'Исходы по таймам (1-й тайм)', '', 'Мен', '*'), _check_yellow_cards_first_period_total_lesser ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', '', 'Бол', '*'), _check_yellow_cards_second_period_total_greater ],
        [ 'ЖК', (None, 'Исходы по таймам (2-й тайм)', '', 'Мен', '*'), _check_yellow_cards_second_period_total_lesser ],
        [ 'ЖК', ('ЖК', 'Индивидуальный тотал', '*', 'Бол', '*'), _check_yellow_cards_individual_total_greater ],
        [ 'ЖК', ('ЖК', 'Индивидуальный тотал', '*', 'Мен', '*'), _check_yellow_cards_individual_total_lesser ],
        [ 'ЖК', ('ЖК', 'Индивидуальный тотал 1-й тайм', '*', 'Бол', '*'), _check_yellow_cards_first_period_individual_total_greater ],
        [ 'ЖК', ('ЖК', 'Индивидуальный тотал 1-й тайм', '*', 'Мен', '*'), _check_yellow_cards_first_period_individual_total_lesser ],
        [ 'ЖК', ('ЖК', 'Индивидуальный тотал 2-й тайм', '*', 'Бол', '*'), _check_yellow_cards_second_period_individual_total_greater ],
        [ 'ЖК', ('ЖК', 'Индивидуальный тотал 2-й тайм', '*', 'Мен', '*'), _check_yellow_cards_second_period_individual_total_lesser ]
    ]

    bet_pattern = tuple(bet[0:5])
    for (rule_match_special_word, rule_bet_pattern, rule_lambda) in rules:
        if match_special_word == rule_match_special_word and bet_satisfy(rule_bet_pattern, bet_pattern):
            return rule_lambda(bet, match_special_word, whoscored_match)

    return None
