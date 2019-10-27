<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Adapter\Local;
use phpDocumentor\Reflection\File;
use PHPUnit\Util\Filesystem;

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

//        foreach ($meta_data['languages'] as $key => $value);
//        }

        $responseData = array();
        try {
            $lang1_name = $request->query('lang1');
            $lang2_name = $request->query('lang2');
            $lang1_dir = $meta_data['languages'][$lang1_name]; // ? $meta_data['languages'][$request->query('lang1')] : "";
            $lang2_dir = $meta_data['languages'][$lang2_name]; //[$request->query('lang2')]) ? $meta_data['languages'][$request->query('lang2')] : "";

            $lang1_data = $this->extractJson($resource_dir . $lang1_dir . "/data_types.json");
            $lang2_data = $this->extractJson($resource_dir . $lang2_dir . "/data_types.json");

            $lang_merge = array_map(function($a, $b){ return array($a,$b);}, $lang1_data, $lang2_data);


            $responseData = array(
                "concept" => $request->query('concept'),
                "lang1" => $lang1_name,
                "lang2" => $lang2_name,
                "lang1_shortname" => $lang1_dir,
                "lang2_shortname" => $lang2_dir,
                "concepts" => ["Concept 1", "Concept 2", "Concept 3"],
                "lang1Concepts" => $lang1_data["data_types"][0]["numerical"],
                "lang2Concepts" => $lang2_data["data_types"][0]["numerical"],
            );

        }
        catch (Exception $exception) {
            // TODO: Add better error handling (404 page perhaps?)
            die("Bad language options!: " . $exception->getMessage());
        }

        return view('compare', $responseData);
    }

//    /**
//     * Show the form for creating a new resource.
//     *
//     * @return \Illuminate\Http\Response
//     */
//    public function create()
//    {
//        //
//    }

//    /**
//     * Store a newly created resource in storage.
//     *
//     * @param  \Illuminate\Http\Request  $request
//     * @return \Illuminate\Http\Response
//     */
//    public function store(Request $request)
//    {
//        //
//    }

    /**
     * Display the specified resource.
     *
     * @param string    $id1
     * @param string    $id2
     * @return \Illuminate\Http\Response
     */
    public function show($id1, $id2 = null)
    {
        $message = "Lang 1 is " . $id1 . ", and Lang 2 is " . $id2;

        return new Response($message);
    }

//    /**
//     * Show the form for editing the specified resource.
//     *
//     * @param  int  $id
//     * @return \Illuminate\Http\Response
//     */
//    public function edit($id)
//    {
//        //
//    }

//    /**
//     * Update the specified resource in storage.
//     *
//     * @param  \Illuminate\Http\Request  $request
//     * @param  int  $id
//     * @return \Illuminate\Http\Response
//     */
//    public function update(Request $request, $id)
//    {
//        //
//    }

//    /**
//     * Remove the specified resource from storage.
//     *
//     * @param  int  $id
//     * @return \Illuminate\Http\Response
//     */
//    public function destroy($id)
//    {
//        //
//    }
}
