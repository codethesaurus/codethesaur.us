app.get('/yourpage', async (req, res) => {
    // Log the visit to the database
    await db.query("INSERT INTO visit_stats (page_name) VALUES ('yourpage')");
    
    // Render or send response for the page
    res.render('yourpage');
});
