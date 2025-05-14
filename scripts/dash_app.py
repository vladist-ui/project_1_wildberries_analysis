import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Инициализация Dash-приложения
class app_dashbord():
    def __init__(self, df):
        self.app = dash.Dash(__name__, suppress_callback_exceptions=True)

        # Лейаут дэшборда
        self.app.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            
            # Навигационное меню
            html.Div([
                dcc.Link('Главная', href='/', style={'margin-right': '20px'}),
                dcc.Link('Данные', href='/data', style={'margin-right': '20px'}),
                dcc.Link('EDA', href='/eda', style={'margin-right': '20px'}),
                dcc.Link('Тренды', href='/trends', style={'margin-right': '20px'}),
                dcc.Link('Выводы', href='/conclusions', style={'margin-right': '20px'}),
            ], style={'padding': '20px', 'background-color': '#f8f9fa', 'border-bottom': '1px solid #dee2e6'}),
            
            # Контент страницы
            html.Div(id='page-content', style={'padding': '20px'})
        ])

        # Главная страница
        index_page = html.Div([
            html.H1("Анализ товаров Wildberries", style={'textAlign': 'center'}),
            html.Hr(),
            html.Div([
                html.H3("Описание проекта"),
                html.P("Этот дэшборд предоставляет анализ зависимости рейтинга популярных товаров на Wildberries от количества отзывов и ценовой категории."),
                html.P("Основные возможности:"),
                html.Ul([
                    html.Li("Просмотр и фильтрация данных"),
                    html.Li("Исследовательский анализ данных (EDA)"),
                    html.Li("Выявление трендов и закономерностей"),
                    html.Li("Получение выводов ")
                ]),
                html.H3("Источник данных"),
                html.P("Данные были собраны с Selenium и содержат информацию о:"),
                html.Ul([
                    html.Li("Названиях товаров"),
                    html.Li("Ценах"),
                    html.Li("Рейтингах"),
                    html.Li("Количестве отзывов"),
                    html.Li("Ссылках на товары")
                ])
            ])
        ])

        # Раздел "Данные"
        data_page = html.Div([
            html.H1("Данные", style={'textAlign': 'center'}),
            html.Hr(),
            
            # Счетчики и метрики
            html.Div([
                html.Div([
                    html.H4("Общее количество записей"),
                    html.H3(id='total-records')
                ], style={'width': '30%', 'display': 'inline-block', 'text-align': 'center', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
                
                html.Div([
                    html.H4("Количество пропусков"),
                    html.H3(id='missing-values')
                ], style={'width': '30%', 'display': 'inline-block', 'text-align': 'center', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
                
                html.Div([
                    html.H4("Уникальные категории"),
                    html.H3(id='unique-categories')
                ], style={'width': '30%', 'display': 'inline-block', 'text-align': 'center', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'})
            ], style={'margin-bottom': '30px'}),
            
            # Визуализации распределений
            html.Div([
                html.Div([
                    dcc.Graph(id='price-distribution',
                             config={'displayModeBar': False},
                             style={'height': '400px'})
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(id='category-distribution',
                             config={'displayModeBar': False},
                             style={'height': '400px'})
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'float': 'right'})
            ], style={'margin-bottom': '30px'}),
            
            # Интерактивная таблица
            html.Div([
                html.H3("Фильтрация данных", style={'margin-bottom': '15px'}),
                html.Div([
                    dcc.Dropdown(
                        id='data-category-filter',
                        options=[{'label': cat, 'value': cat} for cat in sorted(df['req'].unique())],
                        placeholder="Выберите категорию(и)",
                        multi=True,
                        clearable=True,
                        style={'width': '100%'}
                    )
                ], style={'width': '50%', 'margin-bottom': '20px'}),
                
                html.Div([
                    dash_table.DataTable(
                        id='data-table',
                        columns=[{'name': col, 'id': col} for col in df.columns if col != 'id'],
                        page_size=10,
                        filter_action="native",
                        sort_action="native",
                        sort_mode="multi",
                        page_action="native",
                        style_table={
                            'overflowX': 'auto',
                            'border': '1px solid #ddd',
                            'border-radius': '5px'
                        },
                        style_cell={
                            'textAlign': 'left',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'minWidth': '100px',
                            'padding': '8px'
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold',
                            'border': '1px solid #ddd'
                        },
                        style_data={
                            'border': '1px solid #ddd'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ]
                    )
                ], style={'margin-top': '20px'})
            ])
        ])

        # Раздел "EDA"
        eda_page = html.Div([
            html.H1("Первичный анализ данных (EDA)", style={'textAlign': 'center'}),
            html.Hr(),
            
            html.Div([
                html.Div([
                    html.H3("Статистические характеристики"),
                    html.Div(id='statistics-table')
                ], style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
                
                html.Div([
                    html.H3("Корреляционный анализ"),
                    dcc.Graph(id='correlation-heatmap')
                ], style={'width': '50%', 'display': 'inline-block'})
            ]),
            
            html.Div([
                html.H3("Анализ распределений"),
                dcc.Dropdown(
                    id='eda-feature-selector',
                    options=[{'label': col, 'value': col} for col in ['price', 'rating', 'reviews']],
                    value='price',
                    clearable=False
                ),
                dcc.Graph(id='feature-distribution')
            ]),
            
            html.Div([
                html.H3("Анализ выбросов"),
                dcc.Graph(id='outliers-boxplot')
            ])
        ])

        # Раздел "Тренды и закономерности"
        trends_page = html.Div([
            html.H1("Анализ трендов по ценовым квартилям", style={'textAlign': 'center', 'margin-bottom': '20px'}),
            html.Hr(),
            
            # Фильтры и настройки
            html.Div([
                html.Div([
                    html.Label("Выберите категории для сравнения:", style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='trends-category-filter',
                        options=[{'label': cat, 'value': cat} for cat in sorted(df['req'].unique())],
                        value=sorted(df['req'].unique()),
                        multi=True,
                        clearable=False,
                        style={'width': '100%'}
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'padding-right': '20px'}),
                
                html.Div([
                    html.Label("Анализируемый показатель:", style={'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='metric-selector',
                        options=[
                            {'label': 'Средний рейтинг', 'value': 'rating'},
                            {'label': 'Количество отзывов', 'value': 'reviews'},
                            {'label': 'Кол-во товаров', 'value': 'count'}
                        ],
                        value='rating',
                        clearable=False,
                        style={'width': '100%'}
                    )
                ], style={'width': '30%', 'display': 'inline-block', 'padding-right': '20px'}),
                
                html.Div([
                    html.Label("Тип анализа:", style={'font-weight': 'bold'}),
                    dcc.RadioItems(
                        id='analysis-type',
                        options=[
                            {'label': 'По квартилям внутри категории', 'value': 'category'}
                        ],
                        value='category',
                        inline=True,
                        style={'margin-top': '5px'}
                    )
                ], style={'width': '30%', 'display': 'inline-block'})
            ], style={'margin-bottom': '30px', 'padding': '15px', 'background': '#f8f9fa', 'border-radius': '5px'}),
            
            # Основные графики
            html.Div([
                dcc.Graph(
                    id='price-quartiles-comparison',
                    style={'height': '500px', 'border': '1px solid #ddd', 'border-radius': '5px'}
                )
            ], style={'margin-bottom': '30px'}),
            
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='metric-by-quartile',
                        style={'height': '400px', 'border': '1px solid #ddd', 'border-radius': '5px'}
                    )
                ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    dcc.Graph(
                        id='category-distribution-quartiles',
                        style={'height': '400px', 'border': '1px solid #ddd', 'border-radius': '5px'}
                    )
                ], style={'width': '48%', 'display': 'inline-block', 'float': 'right', 'padding': '10px'})
            ]),
            
            # Таблица с квартильными границами
            html.Div([
                html.H3("Границы ценовых квартилей по категориям"),
                dash_table.DataTable(
                    id='quartiles-table',
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'center',
                        'padding': '8px'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    }
                )
            ], style={'margin-top': '30px'})
        ])

        # Раздел "Выводы и рекомендации"
        conclusions_page = html.Div([
            html.H1("Выводы", style={'textAlign': 'center'}),
            html.Hr(),
            
            html.Div([
                html.Div([
                    html.H3("Ключевые инсайты"),
                    html.Ul([
                        html.Li("Корреляций мкжду ценой, рейтингом и кол-вом отзывов не наблюдается в датасете"),
                        html.Li("У джинс и часов с возрастанием цены растёт рейтинг. Скорее всего, это связанно с тем, что продавцы предлагают дешёвый некачественные товар(дорогие наушики будут очень сильно отличаться от дешёвых)"),
                        html.Li("У некотрых товаров есть связь рейтинга и стоимости, а у некотрых нет. Так что нельзя сказать однозначно про связь стоимости и рейтинга, но на некоторых товарах не стоит экономить"),
                        html.Li("Распределение рейтинга смещено влево, возможно это из-за того что покупателям изначально понравился товар, а после покупки, они оставляют хороший отзыв"),
                        html.Li("Футболки лидируют по количеству отзывов во всех ценовых сегментах, так как их больше покупают"),
                        html.Li("нет связи между оценкой товара и количеством отзывов, что видно в корреляционном анализе")
                    ])
                ])
                ], style={'width': '50%', 'display': 'inline-block', 'padding-right': '20px'}),
            
            html.Div([
                html.H3("Улучшение проекта"),
                html.Ol([
                    html.Li("Сбор большего объёма данных по большему числу товаров для более объективной оценки"),
                    html.Li("Модернизация парсера(заменить использование time.sleep на Webdriverwaight или asyncio.sleep)"),
                    html.Li("Использовать async или multiprocessing для запуска нескольких дра1йвверов одновременно")
                ])
            ], style={'margin-top': '30px'})
        ])

        # Обновление страницы
        @self.app.callback(
            Output('page-content', 'children'),
            [Input('url', 'pathname')]
        )
        def display_page(pathname):
            if pathname == '/data':
                return data_page
            elif pathname == '/eda':
                return eda_page
            elif pathname == '/trends':
                return trends_page
            elif pathname == '/conclusions':
                return conclusions_page
            else:
                return index_page

        # Колбэки для раздела "Данные"
        @self.app.callback(
            [Output('total-records', 'children'),
             Output('missing-values', 'children'),
             Output('unique-categories', 'children'),
             Output('price-distribution', 'figure'),
             Output('category-distribution', 'figure'),
             Output('data-table', 'data')],
            [Input('data-category-filter', 'value')]
        )
        def update_data_section(selected_categories):
            if selected_categories and len(selected_categories) > 0:
                filtered_df = df[df['req'].isin(selected_categories)]
            else:
                filtered_df = df.copy()
            
            # Метрики
            total_records = len(filtered_df)
            missing_values = filtered_df.isnull().sum().sum()
            unique_categories = len(filtered_df['req'].unique())
            
            # Графики
            price_fig = px.histogram(
                filtered_df, x='price', 
                title='Распределение цен',
                nbins=20,
                color_discrete_sequence=['#3498db']
            )
            price_fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20)
            )
            
            category_fig = px.bar(
                filtered_df['req'].value_counts().reset_index(), 
                x='req', y='count',
                title='Распределение по категориям',
                color_discrete_sequence=['#2ecc71']
            )
            category_fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis_title="Категория",
                yaxis_title="Количество товаров"
            )
            
            return (
                total_records,
                missing_values,
                unique_categories,
                price_fig,
                category_fig,
                filtered_df.to_dict('records')
            )

        # Колбэки для раздела "EDA"
        @self.app.callback(
            [Output('statistics-table', 'children'),
             Output('correlation-heatmap', 'figure'),
             Output('feature-distribution', 'figure'),
             Output('outliers-boxplot', 'figure')],
            [Input('eda-feature-selector', 'value')]
        )
        def update_eda_page(feature):
            # Статистическая таблица
            stats_df = df.describe().reset_index()
            stats_table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in stats_df.columns],
                data=stats_df.to_dict('records'),
                style_cell={'textAlign': 'center'}
            )
            
            # Тепловая карта корреляций
            corr = df.select_dtypes(include=np.number).corr()
            corr_fig = px.imshow(corr, text_auto=True, title='Корреляция между числовыми признаками')
            
            # Распределение выбранного признака
            dist_fig = px.histogram(df, x=feature, nbins=20, title=f'Распределение {feature}')
            
            # Ящик с усами
            box_fig = px.box(df, y=feature, title=f'Анализ выбросов для {feature}')
            
            return stats_table, corr_fig, dist_fig, box_fig

        # Колбэки для раздела "Тренды"
        # Колбэк для анализа по квартилям
        @self.app.callback(
            [Output('price-quartiles-comparison', 'figure'),
             Output('metric-by-quartile', 'figure'),
             Output('category-distribution-quartiles', 'figure'),
             Output('quartiles-table', 'data'),
             Output('quartiles-table', 'columns')],
            [Input('trends-category-filter', 'value'),
             Input('metric-selector', 'value'),
             Input('analysis-type', 'value')]
        )
        def update_quartile_analysis(categories, metric, analysis_type):
            try:
                if not categories:
                    raise ValueError("Выберите хотя бы одну категорию")
                
                filtered_df = df[df['req'].isin(categories)].copy()
                
                # Рассчитываем квартили для каждой категории отдельно
                quartiles_data = []
                result_dfs = []
                
                for category in categories:
                    cat_df = filtered_df[filtered_df['req'] == category]
                    
                    if analysis_type == 'category':
                        # Квартили внутри категории
                        quartiles = cat_df['price'].quantile([0, 0.25, 0.5, 0.75, 1]).values
                        cat_df['price_quartile'] = pd.qcut(cat_df['price'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
                    else:
                        # Глобальные квартили
                        quartiles = df['price'].quantile([0, 0.25, 0.5, 0.75, 1]).values
                        cat_df['price_quartile'] = pd.qcut(cat_df['price'], q=quartiles, labels=['Q1', 'Q2', 'Q3', 'Q4'])
                    
                    # Сохраняем границы квартилей
                    quartiles_data.append({
                        'Категория': category,
                        'Q1 (25%)': f"{quartiles[1]:.0f} руб",
                        'Q2 (50%)': f"{quartiles[2]:.0f} руб",
                        'Q3 (75%)': f"{quartiles[3]:.0f} руб",
                        'Max': f"{quartiles[4]:.0f} руб"
                    })
                    
                    result_dfs.append(cat_df)
                
                filtered_df = pd.concat(result_dfs)
                
                # Подготовка данных для графиков
                if metric == 'count':
                    comparison_df = filtered_df.groupby(['req', 'price_quartile']).size().reset_index(name='count')
                    metric_title = 'Количество товаров'
                else:
                    comparison_df = filtered_df.groupby(['req', 'price_quartile'])[metric].mean().reset_index()
                    metric_title = f'Средний {metric}'
                
                # График 1: Сравнение по квартилям
                fig1 = px.bar(
                    comparison_df,
                    x='price_quartile',
                    y=metric,
                    color='req',
                    barmode='group',
                    title=f'Сравнение по ценовым квартилям ({metric_title})',
                    labels={'price_quartile': 'Ценовой квартиль', metric: metric_title},
                    category_orders={'price_quartile': ['Q1', 'Q2', 'Q3', 'Q4']}
                )
                fig1.update_layout(plot_bgcolor='white')
                
                # График 2: Тренд по квартилям
                fig2 = px.line(
                    comparison_df,
                    x='price_quartile',
                    y=metric,
                    color='req',
                    title=f'{metric_title} по ценовым квартилям',
                    markers=True,
                    category_orders={'price_quartile': ['Q1', 'Q2', 'Q3', 'Q4']}
                )
                fig2.update_layout(plot_bgcolor='white')
                
                # График 3: Распределение по квартилям
                dist_df = filtered_df.groupby(['price_quartile', 'req']).size().reset_index(name='count')
                fig3 = px.bar(
                    dist_df,
                    x='price_quartile',
                    y='count',
                    color='req',
                    title='Распределение товаров по квартилям',
                    category_orders={'price_quartile': ['Q1', 'Q2', 'Q3', 'Q4']}
                )
                fig3.update_layout(plot_bgcolor='white')
                
                # Таблица с границами квартилей
                columns = [{'name': col, 'id': col} for col in quartiles_data[0].keys()]
                
                return fig1, fig2, fig3, quartiles_data, columns
            
            except Exception as e:
                error_fig = {
                    'layout': {
                        'title': f'Ошибка: {str(e)}',
                        'xaxis': {'visible': False},
                        'yaxis': {'visible': False},
                        'annotations': [{
                            'text': f'Ошибка: {str(e)}',
                            'xref': 'paper',
                            'yref': 'paper',
                            'showarrow': False,
                            'font': {'size': 16, 'color': 'red'}
                        }],
                        'plot_bgcolor': 'white'
                    }
                }
                return error_fig, error_fig, error_fig, [], []
