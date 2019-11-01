<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class CompareController extends Controller
{
    /**
     * Return an assoc array of the JSON contents of a file
     *
     * @param string $fileName
     * @param bool $assoc
     * @return array
     */
    private function extractJson($fileName, $assoc = true) {
        return json_decode(utf8_encode(file_get_contents($fileName)), $assoc);
    }

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        // Get thesaurus directory
        $resource_dir = resource_path('thesauruses/');

        // Read JSON file
        $meta_data = $this->extractJson($resource_dir . 'meta_info.json');
        $meta_data_langs = $meta_data["languages"];

        $concept = $request->query('concept');
        try {
            $lang1_name = $request->query('lang1');
            $lang2_name = $request->query('lang2');
            $lang1_dir = $meta_data_langs[$lang1_name];
            $lang2_dir = $meta_data_langs[$lang2_name];

            $lang1_data = ($this->extractJson($resource_dir . $lang1_dir . "/" . $concept . ".json"))[$concept];
            $lang2_data = ($this->extractJson($resource_dir . $lang2_dir . "/" . $concept . ".json"))[$concept];

            // Probably not the most efficient way to look for all the categories, but I can fix this later
            // TODO: add category list to JSON files
            $categories = array();
            foreach($lang1_data as $key => $value) {
                if(!in_array($value["category"], $categories)) {
                    array_push($categories, $value["category"]);
                }
            }
            foreach($lang2_data as $key => $value) {
                if(!in_array($value["category"], $categories)) {
                    array_push($categories, $value["category"]);
                }
            }

            $responseData = array(
                "concept" => $concept,
                "lang1" => $lang1_name,
                "lang2" => $lang2_name,
                "lang1_shortname" => $lang1_dir,
                "lang2_shortname" => $lang2_dir,
                "categories" => $categories,
                "lang1Concepts" => $lang1_data,
                "lang2Concepts" => $lang2_data,
            );

        }
        catch (Exception $exception) {
            // TODO: Add better error handling (404 page perhaps?)
            die("Bad language options!: " . $exception->getMessage());
        }

        return view('compare', $responseData);
    }

}
