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

Route::get('/.well-known/acme-challenge/KW6aDeVbrfe2blTE8hOuSUYjw8SS6HOc0xhioHjA1OU', function() {
    return 'KW6aDeVbrfe2blTE8hOuSUYjw8SS6HOc0xhioHjA1OU.2tp1B8sKxN_e8tkWiVmqSJC-F3k17yr6vZOI8DbAl6g';
});
