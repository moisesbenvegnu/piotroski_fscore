# -*- coding: utf-8 -*-
"""
@author: Moises Benvegnu
"""

import streamlit as st
import yfinance as yf
import pandas as pd

st.title('Piotroski F-Score')

st.markdown('Uma forma simples de avaliar a saúde financeira de empresas listadas em bolsa')

st.image('capa.png')

bolsa = st.selectbox('Selecione a bolsa', ['Brasil', 'EUA', 'Frankfurt', 'Paris', 'Amsterdã', 'Oslo', 'Madrid', 'Suécia', 'Japão'])

ticker = st.text_input('Digite o ticker do ativo')

if len(ticker)==0:
    st.info('Aguardando informar o ticker')
else:
    try:
    
        if bolsa == 'Brasil':
            ticker = ticker+'.SA'
        elif bolsa == 'EUA':
            ticker = ticker
        elif bolsa == 'Paris':
            ticker = ticker+'.PA'
        elif bolsa == 'Frankfurt':
            ticker = ticker+'.F'
        elif bolsa == 'Amsterdã':
            ticker = ticker+'.AS'
        elif bolsa == 'Oslo':
            ticker = ticker+'.OL'  
        elif bolsa == 'Madrid':
            ticker = ticker+'.MC'  
        elif bolsa == 'Suécia':
            ticker = ticker+'.ST'  
        elif bolsa == 'Japão':
            ticker = ticker+'.T'
    
        stock = yf.Ticker(ticker.upper())
        infos = stock.info
        balance = stock.balance_sheet
        cashflow = stock.cashflow
        financial = stock.financials
        
        #infos
        name = infos['shortName']
        
        st.info(f'Este ticker corresponde à empresa {name}')
    
        #financials
        net_income_current = financial.loc['Net Income'][0]
        net_income_previous = financial.loc['Net Income'][1]
    
        gross_profit_current = financial.loc['Gross Profit'][0]
        gross_profit_previous = financial.loc['Gross Profit'][1]
    
        total_revenue_current = financial.loc['Total Revenue'][0]
        total_revenue_previous = financial.loc['Total Revenue'][1]
    
        #balance
        total_assets_current = balance.loc['Total Assets'][0]
        total_assets_previous1 = balance.loc['Total Assets'][1]
        total_assets_previous2 = balance.loc['Total Assets'][2]
    
        longtermdebt_current = balance.loc['Long Term Debt'][0]
        longtermdebt_previous = balance.loc['Long Term Debt'][1]
    
        total_current_assets_current = balance.loc['Total Current Assets'][0]
        total_current_assets_previous = balance.loc['Total Current Assets'][1]
    
        total_current_liabilities_current = balance.loc['Total Current Liabilities'][0]
        total_current_liabilities_previous = balance.loc['Total Current Liabilities'][1]
    
        common_stock_current = balance.loc['Common Stock'][0]
        common_stock_previous = balance.loc['Common Stock'][1]
    
        #cashflow
        operating_cashflow = cashflow.loc['Total Cash From Operating Activities'][0]
        
    except:
        st.info('Não há informações disponíveis para este ativo')
    
    try:
        #Criterios Piotroski F-Score    
    
        # 1. Return on Asset (ROA) > 0 (Score +1)
        average_assets1 = (total_assets_current + total_assets_previous1)/2
        
        if net_income_current/average_assets1 > 0:
            score1 = 1
        else:
            score1 = 0
        
        # 2. Operating Cash Flow (OCF) > 0 (Score +1)
        if operating_cashflow > 0:
            score2 = 1
        else:
            score2 = 0
            
        # 3. ROA Current Year  > ROA Previous Year (Score +1)
        if net_income_current/total_assets_current > net_income_previous/total_assets_previous1:
            score3 = 1
        else:
            score3 = 0
        
        # 4. CFO > Net Income (Score +1)
        if operating_cashflow > net_income_current:
            score4 = 1
        else:
            score4 = 0
    
        # 5. Long Term Debt Current Year < Long Term Debt Previous Year (Score +1)
        if longtermdebt_current < longtermdebt_previous:
            score5 = 1
        else:
            score5 = 0
    
        # 6. Current Ratio Current Year > Current Ratio Previous Year (Score +1)
        ratio1 = total_current_assets_current/total_current_liabilities_current
        ratio2 = total_current_assets_previous/total_current_liabilities_previous
    
        if ratio1 > ratio2:
            score6 = 1
        else:
            score6 = 0
    
        # 7. No new shares issued in the last year (Score+1)
        if common_stock_current > common_stock_previous:
            score7 = 0
        else:
            score7 = 1
    
        # 8. Gross Margin Current Year > Gross Margin Previous Year (Score +1)
        gross_margin_current = gross_profit_current/total_revenue_current
        gross_margin_previous = gross_profit_previous/total_revenue_previous
    
        if gross_margin_current > gross_margin_previous:
            score8 = 1
        else:
            score8 = 0
    
        #9. Asset Turnover Ratio Current Year > Asset Turnover Ratio Previous Year (Score + 1)
        average_assets2 = (total_assets_previous1 + total_assets_previous2)/2
    
        turnover_current = total_revenue_current/average_assets1
        turnover_previous = total_revenue_previous/average_assets2
    
        if turnover_current > turnover_previous:
            score9 = 1
        else:
            score9 = 0
    
        F_score = score1 + score2 + score3 + score4 + score5 + score6 + score7 + score8 + score9
    
    except:
        st.info('Não foi possível calcular o Piotroski F-Score')
        
    else:
        st.info(f'O Piotroski F-Score da empresa é {F_score}')
        
        indice = [1,2,3,4,5,6,7,8,9]
    
        criterios = ['Retorno sobre Ativos (ROA) > 0', 
                     'Fluxo de Caixa Operacional (FCO) > 0', 
                     'Aumento do ROA', 
                     'FCO > Lucro Líquido',
                     'Diminuição da Alavancagem',
                     'Aumento da Liquidez Corrente',
                     'Sem emissão de novas ações',
                     'Aumento da Margem Bruta',
                     'Aumento no Giro do Ativo']
    
        score = [score1, score2, score3, score4, score5, score6, score7, score8, score9]
        
        dic = {'Indice': indice, 'Critério': criterios, 'Score': score}
        
        df = pd.DataFrame(dic)
        
        df.set_index('Indice', inplace = True)
        
        st.markdown('Confira abaixo o atendimento a cada critério:')
        
        st.dataframe(data=df)

'''
Importante:
- Este site possui caráter informativo e educacional, e não de recomendação de investimentos.
- O Piotroski F-Score é utilizado para avaliar a saúde financeira da empresa, porém não utilize apenas este indicador para analisar os ativos.
- Os critérios utilizados levam em consideração os dois últimos anos.
- Os dados utilizados foram extraídos do Yahoo Finance.
- Para saber mais sobre este indicador: https://bit.ly/3R2hYRj
'''

st.markdown('Desenvolvido por Moises A. Benvegnu')



