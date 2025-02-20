# Тюнинг модели
В этой папке представлена последовательность шагов, произведённая с целью побить бэйзлайн модели из шага с EDA.

Ссылка на отчёт wandb - https://api.wandb.ai/links/qesh-squad/wcx1gf82. Все эксперименты подписаны нумерацией, которая маппится на описанную ниже структуру.


Ссылка на датасет (необходима для запуска эксперимента 1) - https://www.kaggle.com/competitions/home-credit-default-risk/data

## Шаг 0 - Бэйзлайн
[0_baseline.ipynb](0_baseline.ipynb)
Этот ноутбук описывает механику расчёта метрик бэйзлайна.
Используется фильтрованный выход EDA как датасет для расчёта и циклически запускаемый катбуст для отбора минимума важнейших фич.

## Шаг 1 - Фильтрация выбросов и аномалий
[1_outliers.ipynb](1_outliers.ipynb)
Этот ноутбук частично собирает заново EDA, чтобы очистить итоговый датасет от выбросов и аномалий в данных.
Используются IterativeImputer для заполнения пропусков и IsolationForest поколоночно для фильтрации выбросов и аномалий.

## Шаг 2 - Permutation Feature Selection
[2_permutation.ipynb](2_permutation.ipynb)
Этот ноутбук использует очищенный от выбросов и аномалий датасет, чтобы рассчитать важность по перестановкам.
Базовый набор фич, полученный таким образом, прогоняется циклически через катбуст до сходимости. Сходимость определяется отсутствием фич с важностью менее 0.5.

## Шаг 3 - mRMR
[3_mRMR.ipynb](3_mRMR.ipynb)
Этот ноутбук описывает альтернативный подход к feature selection - “Maximum Relevance — Minimum Redundancy”.

## Шаг 4 - Стэкинг
[4_stacking.ipynb](4_stacking.ipynb)
Этот ноутбук описывает первые две попытки решить задачу классификации стекингом различных алгоритмов. Обнаружено интересное наблюдение о структуре данных - регрессоры справились с задачей лучше классификаторов.

## Шаг 5 - CV
[5_cv.ipynb](5_cv.ipynb)
Этот ноутбук описывает попытки улучшить обобщающую способность модели с помощью кросс-валидации.

## Шаг 6 Тюнинг CatBoost
[6_catboost_tuning.ipynb](6_catboost_tuning.ipynb)
Этот ноутбук описывает различные подходы к тюнингу гиперпараметров алгоритма катбуста. Осторожно, тюнинг и обучение на полном наборе permutation фич очень медленное.

## Шаг 7 Замена модели
[7_lightGBM.ipynb](7_lightGBM.ipynb) Самый успешный шаг.

Ноутбук описывает тюнинг lightGBM с дисбалансом и без, а также рассчитывает соответствующие метрики и финалит артефакты для следующего шага.