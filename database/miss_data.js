const lookupData = async (req, res) => {
    const data = await findData(req.params.id);

    if (!data) {
        // Log missing data into the database
        await db.query("INSERT INTO missing_data_stats (requested_item, missing_reason) VALUES (?, ?)", [req.params.id, 'Data not found']);
        res.status(404).send('Data not found');
        return;
    }

    res.send(data);
};
