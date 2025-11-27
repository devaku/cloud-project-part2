import azure.functions as func
import routes.debug, routes.images, routes.nutrition, routes.database
# import routes.nutrition if needed

app = func.FunctionApp()

# User Auth
app.route(route="login", auth_level=func.AuthLevel.ANONYMOUS)(routes.database.login)
app.route(route="logout", auth_level=func.AuthLevel.ANONYMOUS)(routes.database.logout)
app.route(route="register", auth_level=func.AuthLevel.ANONYMOUS)(routes.database.register)
app.route(route="verifyLogin", auth_level=func.AuthLevel.ANONYMOUS)(routes.database.verifyLogin)

# Debug routes
app.route(route="debug", auth_level=func.AuthLevel.ANONYMOUS)(routes.debug.debug)

# Image routes
app.route(route="images/heatmap", auth_level=func.AuthLevel.ANONYMOUS)(routes.images.getHeatmap)
app.route(route="images/barchart", auth_level=func.AuthLevel.ANONYMOUS)(routes.images.getBarchart)
app.route(route="images/scatterplot", auth_level=func.AuthLevel.ANONYMOUS)(routes.images.getScatterplot)

# Uncomment later if you add nutrition again
app.route(route="process", auth_level=func.AuthLevel.ANONYMOUS)(routes.nutrition.processNutrition)
app.route(route="getAll", auth_level=func.AuthLevel.ANONYMOUS)(routes.nutrition.getAllData)
