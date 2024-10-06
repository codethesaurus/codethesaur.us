app.get('/stats', async (req, res) => {
    const visitStats = await db.query("SELECT page_name, COUNT(*) as visit_count FROM visit_stats GROUP BY page_name");
    const missingDataStats = await db.query("SELECT requested_item, COUNT(*) as missing_count FROM missing_data_stats GROUP BY requested_item");

    res.render('stats', { visitStats, missingDataStats });
});
