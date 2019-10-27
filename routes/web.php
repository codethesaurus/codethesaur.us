<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::get('/about', function () {
    return view('about');
});

Route::resource('compare', 'CompareController');

Route::get('compare/{id}', 'CompareController@show');   // should this be index?
Route::get('compare/{id1}/{id2}', 'CompareController@show');   // should this also be index?
