import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import RobustScaler, StandardScaler


def data_prepare(df, cls_id_selected=12, yr_crit=2019):
        """
        讀取資料，依據資料欄位篩選變量
        取cluster_id list成{}，取出想要預測的cluster_id
        不取第一欄的clister_id>>>[1:]
        把x變量跟y變量的資料取出
        針對x變量標準化後取出
        """
        # ##########################
        # Split data into clusters #
        # ##########################
        #df = df.rename(columns={'count':'cnt'})
        #df.groupby('Cluster_id').count().sort_values('Year',ascending=False)

        # check a cluster peak by index
        cls_ids = df["Cluster_id"].unique()

        cluster = {}
        for cls_id in cls_ids:
                cluster[cls_id] = df[df['Cluster_id']==cls_id].iloc[:,1:]

        assert len(cluster.keys()) == len(cls_ids)

        train = cluster[cls_id_selected][cluster[cls_id_selected]['Year'] < yr_crit]
        test = cluster[cls_id_selected][cluster[cls_id_selected]['Year'] == yr_crit]
        print("INFO: TRAIN/TEST shape BEFORE scaling:", train.shape, test.shape)

        # #######################################
        # Fetch the train & test column indices #
        # #######################################
        cols = list(df.columns)[1:]
        x_col_ids = []
        for idx, b in zip(np.arange(100), np.array(cols) != "Pickup_count"):
                #     print(idx, b)
                if b == True:
                        x_col_ids.append(idx)

        y_col_id = np.argmax(np.array(cols) == "Pickup_count")

        # #############
        # X & y split #
        # #############
        train_x = train.values[:, x_col_ids]
        train_y = train.values[:, y_col_id]

        test_x = test.values[:, x_col_ids]
        test_y = test.values[:, y_col_id]

        # ######################
        # Data Standarlization #
        # ######################
        scaler =  StandardScaler()
        # scaler =  RobustScaler()
        scaler = scaler.fit(train_x)

        train_x_scaled = scaler.transform(train_x)
        test_x_scaled = scaler.transform(test_x)
        print("INFO: shape of scaled TRAIN_X and TEST_X:", train_x_scaled.shape, test_x_scaled.shape)

        print("INFO: shape of TRAIN_Y and TEST_Y:", train_y.shape, test_y.shape)

        assert len(train_y) == len(train_x_scaled) == len(train_x)
        assert len(test_y) == len(test_x_scaled) == len(test_x)

        return train_x_scaled, train_y, test_x_scaled, test_y


def time_window_strided_sampling(X,y, time_steps=1):
        """
        這裡是要把過去的資料加到現在的資料中當作變量
        時間步數是根據自設的參數調整有所差別 以1的表現比較好
        """
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
                v = X[i:(i + time_steps)]
                Xs.append(v)
                ys.append(y[i + time_steps])
        return np.array(Xs), np.array(ys)