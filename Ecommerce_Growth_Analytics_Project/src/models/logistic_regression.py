# src/models/logistic_regression.py

import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (

    accuracy_score,

    classification_report,

    confusion_matrix,

    roc_curve,

    auc

)


class ChurnPredictor:

    def __init__(self):
        # 检查文件是否存在
        file_path = "data/processed/churn_dataset.csv"
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"请先运行 ChurnAnalysis 生成数据集: {file_path}"
            )
        self.df = pd.read_csv(file_path)

    # ==================================
    # 数据准备
    # ==================================

    def prepare_data(self):

        X = self.df.drop(

            [

                "user_id",

                "last_order_date",
                "days_since_last_order",
                "churn"

            ],

            axis=1,

            errors="ignore"

        )

        y = self.df["churn"]

        return train_test_split(

            X,

            y,

            test_size=0.2,

            random_state=42,

            stratify=y

        )

    # ==================================
    # 模型训练
    # ==================================

    def train_model(self):

        X_train, X_test, y_train, y_test = (

            self.prepare_data()

        )

        model = LogisticRegression(

            max_iter=1000

        )

        model.fit(

            X_train,

            y_train

        )

        pred = model.predict(

            X_test

        )

        prob = model.predict_proba(

            X_test

        )[:, 1]

        print(

            "\nAccuracy:"

        )

        print(

            accuracy_score(

                y_test,

                pred

            )

        )

        print(

            "\nClassification Report"

        )

        print(

            classification_report(

                y_test,

                pred

            )

        )

        print(

            "\nConfusion Matrix"

        )

        print(

            confusion_matrix(

                y_test,

                pred

            )

        )

        self.plot_roc(

            y_test,

            prob

        )

        self.feature_importance(

            model,

            X_train.columns

        )

    # ==================================
    # ROC曲线
    # ==================================

    def plot_roc(

        self,

        y_true,

        y_prob

    ):

        fpr, tpr, _ = roc_curve(

            y_true,

            y_prob

        )

        roc_auc = auc(

            fpr,

            tpr

        )

        plt.figure(

            figsize=(8, 6)

        )

        plt.plot(

            fpr,

            tpr,

            label=f"AUC={roc_auc:.3f}"

        )

        plt.plot(

            [0, 1],

            [0, 1]

        )

        plt.xlabel(

            "False Positive Rate"

        )

        plt.ylabel(

            "True Positive Rate"

        )

        plt.title(

            "ROC Curve"

        )

        plt.legend()

        plt.savefig(

            "reports/figures/churn_roc_curve.png"

        )

        plt.close()

        print(

            f"\nAUC={roc_auc:.3f}"

        )

    # ==================================
    # 特征重要性
    # ==================================

    def feature_importance(

        self,

        model,

        columns

    ):

        importance = pd.DataFrame(

            {

                "feature": columns,

                "coef": model.coef_[0]

            }

        )

        importance = importance.sort_values(

            by="coef",

            ascending=False

        )

        print(

            "\nTop特征"

        )

        print(

            importance.head(15)

        )

    def run(self):

        self.train_model()


if __name__ == "__main__":

    ChurnPredictor().run()