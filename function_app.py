import azure.functions as func
import routes.debug, routes.images
# routes.nutrition

app = func.FunctionApp()
app.route(route="debug", auth_level=func.AuthLevel.ANONYMOUS)(routes.debug.debug)
# app.route(route="process", auth_level=func.AuthLevel.ANONYMOUS)(routes.nutrition.processNutrition)
app.route(route="images/heatmap", auth_level=func.AuthLevel.ANONYMOUS)(routes.images.getHeatmap)
app.route(route="images/barchart", auth_level=func.AuthLevel.ANONYMOUS)(routes.images.getBarchart)
app.route(route="images/scatterplot", auth_level=func.AuthLevel.ANONYMOUS)(routes.images.getScatterplot)
    