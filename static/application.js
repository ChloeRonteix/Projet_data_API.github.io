function display_news(json_movies) {
    console.log("Résultat de la requête :", json_movies);
    news_data = json_movies["data"];
    console.log(json_movies["articles"].length);
    console.log(json_movies["keywords"][0]["word"]);
    
}