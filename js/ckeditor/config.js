/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here.
	// For complete reference see:
	// http://docs.ckeditor.com/#!/api/CKEDITOR.config

	// The toolbar groups arrangement, optimized for two toolbar rows.
	config.removePlugins='forms,iframe,showblocks,language,templates,bidi,documentproperties,stylescombo,div,elementspath,specialchar,liststyle';
	config.enterMode = CKEDITOR.ENTER_BR;
	config.codeSnippet_theme='magula';
// 	config.toolbar='notebook';
// 	config.toolbar_notebook =
// [
// 	{ name: 'editing', items : [ 'Undo','Redo','-','Find','Replace','-','SelectAll' ] },
// 	{ name: 'clipboard', items:['PasteText','PasteFromWord']},
// 	{ name: 'tools', items : [ 'Maximize', 'ShowBlocks','-','Source','About' ] },
// 	{ name: 'links', items : [ 'Link','Unlink','Anchor','ArticleLink','-','InsertPic'] },
// 	{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript']},
// 	{ name: 'styles', items : [ 'Font','FontSize'] },
// 	{ name: 'insert', items : [ 'Image','Table','HorizontalRule','SpecialChar','PageBreak','Iframe' ] },
// 	{ name: 'expstyles', items:['TextColor','BGColor','-','RemoveFormat' ] },
// 	{ name: 'colors', items : []},
// 	{ name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv']},
// 	{ name: 'align', 'items': ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'] },

// ];

config.toolbarGroups = [
	{ name: 'document', groups: [ 'mode', 'document', 'doctools' ] },
	{ name: 'clipboard', groups: [ 'clipboard', 'undo' ] },
	{ name: 'editing', groups: [ 'find', 'selection', 'spellchecker' ] },
	{ name: 'forms' },
	{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
	{ name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
	{ name: 'links' },
	{ name: 'insert' },
	{ name: 'styles' },
	{ name: 'colors' },
	{ name: 'tools' },
	{ name: 'others' },
	{ name: 'about' }
];

	// Remove some buttons provided by the standard plugins, which are
	// not needed in the Standard(s) toolbar.
	config.removeButtons = 'ShowBlocks,Preview,Language,Zoom,Maximize,About';

	// Set the most common block elements.
	config.format_tags = 'p;h1;h2;h3;pre';

	// Simplify the dialog windows.
	config.removeDialogTabs = 'image:advanced;link:advanced';
};
