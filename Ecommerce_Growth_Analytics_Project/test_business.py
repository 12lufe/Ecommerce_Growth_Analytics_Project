from src.analysis.business_overview import BusinessOverview
from src.analysis.rfm_analysis import RFMAnalysis
from src.analysis.abc_analysis import ABCAnalysis
from src.analysis.product_association_analysis import ProductAssociationAnalysis
from src.analysis.funnel_analysis import FunnelAnalysis
from src.analysis.user_growth_analysis import UserGrowthAnalysis
from src.analysis.churn_analysis import ChurnAnalysis
from src.models.logistic_regression import ChurnPredictor


#BusinessOverview().run()

#RFMAnalysis().run()

#ABCAnalysis().run()

#ProductAssociationAnalysis().run()

#FunnelAnalysis().run()

#UserGrowthAnalysis().run()

ChurnAnalysis().run()

ChurnPredictor().run()