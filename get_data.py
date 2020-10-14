# -*- coding: UTF-8 -*-
import http.client
import json
import time,sys, platform,os,codecs

LEAGUE_IDS = {
    "PL": 'Premiere League',
    "BL1": '1. Bundesliga',
    "FL1": 'Ligue 1',
    "PPL": 'Primeira Liga',
    "PD": 'Primera Division',
    "SA": 'Serie A',
    "CL": 'Champions-League'
    }

f1 = None

def define_f1(nome=None,):
    global f1
    if nome is None:
        f1 = None
    else:
        f1=open(nome,"w",encoding="cp65001")

def escreve_f1(texto):
    global f1
    f1.write(texto+"\n")


def close_f1():
    global f1
    f1.close()

def get_dados_tabela(i,dados):
    position = dados['position']
    team = dados['team']['name']
    played = dados['playedGames']
    won = dados['won']
    draw = dados['draw']
    lost = dados['lost']
    goalsFor = dados['goalsFor']
    goalsAgainst = dados['goalsAgainst']
    goalsDiff = dados['goalDifference']
    return str(position).rjust(2)+" "*6+";"+team.ljust(30)+";"+str(played).rjust(2)+" "*3+";"+str(won).rjust(2)+" "*2+";"+str(draw).rjust(2)+" "*3+";"+str(lost).rjust(2)+" "*5+";"+str(goalsFor).rjust(3)+" "*9+";"+str(goalsAgainst).rjust(3)+" "*11+";"+str(goalsDiff).rjust(4)

def get_dados_marcadores(i,dados):
    position = i+1
    player_name = dados['player']['name']
    team = dados['team']['name']
    goals = dados['numberOfGoals']
    return str(position).rjust(2)+" "*6+";"+player_name.ljust(30)+";"+team.ljust(30)+";"+str(goals).rjust(2)

def get_dados_jogos(i,dados):
    matchday = dados['matchday']
    event_date = dados['utcDate']
    status = dados['status']
    homeTeam = dados['homeTeam']['name']
    awayTeam = dados['awayTeam']['name']
    winner = ""
    result=""

    if status == 'FINISHED':
        winner = dados['score']['winner']
        fullTime = dados['score']['fullTime']
        result = str(fullTime['homeTeam'])+" : "+str(fullTime['awayTeam'])

    return str(matchday).rjust(2)+" "*7+";"+status.ljust(10)+";"+event_date+";"+homeTeam.ljust(30)+";"+awayTeam.ljust(30)+";"+winner.ljust(9)+";"+result


def conn_api():
    try:
        return http.client.HTTPConnection('api.football-data.org')
    except:
        return None

def get_data_testing(conn,team,season=0,status=None):
    try:
        headers = {'X-Auth-Token':'your_Api_Key'}
        str_req = "/v2/competitions/"+team+"/matches/"
        if season > 0:
            str_req += "?season="+str(season)
        if status:
             str_req += "?status="+str(status)
        conn.request('GET',str_req,None,headers)
        return json.loads(conn.getresponse().read().decode())
    except:
        return None


def get_scorers(conn,league,season=0):
    try:
        headers = {'X-Auth-Token':'your_Api_Key'}
        str_req = "/v2/competitions/"+league+"/scorers/"
        if season > 0:
            str_req += "?season="+str(season)

        conn.request('GET',str_req,None,headers)
        return json.loads(conn.getresponse().read().decode())
    except:
        return None

def get_standings(conn,league,season=0):
    try:
        headers = {'X-Auth-Token':'your_Api_Key'}
        str_req = "/v2/competitions/"+league+"/standings/"
        if season > 0:
            str_req += "?season="+str(season)

        conn.request('GET',str_req,None,headers)
        return json.loads(conn.getresponse().read().decode())
    except:
        return None

def get_matches(conn,league,season=0,status=None):
    try:
        headers = {'X-Auth-Token':'your_Api_Key'}
        str_req = "/v2/competitions/"+league+"/matches/"
        if season > 0:
            str_req += "?season="+str(season)
        if status:
             str_req += "?status="+str(status)
        conn.request('GET',str_req,None,headers)
        return json.loads(conn.getresponse().read().decode())
    except:
        return None

def get_data_league_scorers(conn,code_league,season_league=0):
    if conn:
        response = get_scorers(conn,code_league,season_league)
        if "errorCode" in response or "error" in response:
            print("Erro to call get_scorers whit parametrs (League = "+code_league+", Season = "+str(season_league)+")\nError => "+ response['message']+"\n")
        else:
            print("-- League("+code_league+","+str(season_league)+") -> get_dados_marcadores ------------------------------------------------------------------------")
            for p_scorers,data_table in enumerate(response['scorers']):
                text = str(season_league).rjust(4)+";"+LEAGUE_IDS.get(code_league).ljust(20)+";"+get_dados_marcadores(p_scorers,data_table)
                escreve_f1(text)

def get_data_league_standings(conn,code_league,season_league=0):
    if conn:
        response = get_standings(conn,code_league,season_league)
        if "errorCode" in response or "error" in response:
            print("Erro to call get_standings whit parametrs (League = "+code_league+", Season = "+str(season_league)+")\nError => "+ response['message']+"\n")
        else:
            print("-- League("+code_league+","+str(season_league)+") -> get_dados_tabela ----------------------------------------------------------------------------")
            for i_standing in range(len(response['standings'])):
                if response['standings'][i_standing]['type'].upper() == "TOTAL":
                    for p_table,data_table in enumerate(response['standings'][i_standing]['table']):
                        text = str(season_league).rjust(4)+";"+LEAGUE_IDS.get(code_league).ljust(20)+";"+get_dados_tabela(p_table,data_table)
                        escreve_f1(text)

def get_data_league_matches(conn,code_league,season_league=0,status_league=None):
    if conn:
        response = get_matches(conn,code_league,season_league,status_league)
        if "errorCode" in response or "error" in response:
            print("Erro to call get_matches whit parametrs (League = "+code_league+", Season = "+str(season_league)+")\nError => "+ response['message']+"\n")
        else:
            print("-- League("+code_league+","+str(season_league)+") -> get_dados_jogos -----------------------------------------------------------------------------")
            print("Year;League"+" "*14+";Match Day;Status"+" "*4+";Event DateTime"+" "*6+";Home Team"+" "*21+";Away Team"+" "*21+";Winner"+" "*3+";Result")
            for p_table,data_table in enumerate(response['matches']):
                text = str(season_league).rjust(4)+";"+LEAGUE_IDS.get(code_league).ljust(20)+";"+get_dados_jogos(p_table,data_table)
                print(text)
                escreve_f1(text)

def get_data_teste(conn,code_league,season_league=0,status_league=None):
    if conn:
        response = get_data_testing(conn,code_league,season_league,status_league)
        if "errorCode" in response or "error" in response:
            print("Erro to call get_data_testing whit parametrs (League = "+code_league+", Season = "+str(season_league)+", Status = "+str(status_league)+")\nError => "+ response['message']+"\n")
        else:
            print('----------------------------------------------------------------------------------------------------')
            print(response)
            print('----------------------------------------------------------------------------------------------------')

def main():
    leagues = ['PL','FL1','BL1','SA','PPL','PD','CL']

    conn = conn_api()
    limit_calls_minute = 10
    secounds_sleep = 60
    # get_data_league(conn,'BL1',2020)
    # get_data_teste(conn,leagues[4],0,'SCHEDULED')
    # get_data_league_matches(conn,leagues[4],0,)

    i = 0
    define_f1("Tabela_Cassificativa.txt")
    escreve_f1("Year;League"+" "*14+";Position;Team"+" "*26+";Games;Wins;Draws;Defeats;Goals Scored;Conceded Goals;Goals Difference")
    for year in range(2020,2021,1):
        for league in leagues:
            get_data_league_standings(conn,league,year)
            i +=1

            if i == limit_calls_minute:
                print("pause "+str(secounds_sleep)+" secounds ...")
                time.sleep(secounds_sleep)
                i=0
    close_f1()
    define_f1("Lista_Melhores_Marcadores.txt")
    escreve_f1("Year;League"+" "*14+";Position;Player Name"+" "*19+";Team"+" "*26+";Goals")
    for year in range(2020,2021,1):
        for league in leagues:
            get_data_league_scorers(conn,league,year)
            i +=1

            if i == limit_calls_minute:
                print("pause "+str(secounds_sleep)+" secounds ...")
                time.sleep(secounds_sleep)
                i=0
    close_f1()
    define_f1("Dados Campeonato.txt")
    escreve_f1("Year;League"+" "*14+";Match Day;Status"+" "*4+";Event DateTime"+" "*6+";Home Team"+" "*21+";Away Team"+" "*21+";Winner"+" "*3+";Result")
    for year in range(2020,2021,1):
        for league in leagues:        
            get_data_league_matches(conn,league,year,None)
            i +=1

            if i == limit_calls_minute:
                print("pause "+str(secounds_sleep)+" secounds ...")
                time.sleep(secounds_sleep)
                i=0
    close_f1()
    


if __name__ == "__main__":  
    main()