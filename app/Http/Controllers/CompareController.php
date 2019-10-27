<?php

namespace App\Http\Controllers;

use http\Exception\UnexpectedValueException;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Storage;
use League\Flysystem\Adapter\Local;
use phpDocumentor\Reflection\File;
use PHPUnit\Util\Filesystem;
use function MongoDB\BSON\toJSON;

class CompareController extends Controller
{
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
        $meta_data_json = file_get_contents($resource_dir . 'meta_info.json');
        $meta_data = json_decode($meta_data_json,true);

//        foreach ($meta_data['languages'] as $key => $value);
//        }

        if (!isset( $meta_data['languages'][$request->query('lang1')]) || !isset( $meta_data['languages'][$request->query('lang2')])){
            throw new UnexpectedValueException("One of the passed in languages doesn't exist");
        }

        $responseData = array(
            // TODO: delete this eventually
//            "resources" => $languages,
            "concept" => $request->query('concept'),
            "lang1" => $request->query('lang1'),
            "lang2" => $request->query('lang2'),
            "concepts" => ["Concept 1", "Concept 2", "Concept 3"],
            "lang1Concepts" => [
                "Concept 1" => "Concept 1 in lang 1",
                "Concept 2" => "Concept 2 in lang 1",
                "Concept 3" => "Concept 3 in lang 1"
            ],
            "lang2Concepts" => [
                "Concept 1" => "Concept 1 in lang 2",
                "Concept 2" => "Concept 2 in lang 2",
                "Concept 3" => "Concept 3 in lang 2"
            ]
        );
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
