var checkFileExt = function (fileName) {
    var allowedExtension = ['xls', 'xlsx', 'mtd', 'jpg'];
    var fileSp = fileName.split('.');
    var fileEx = fileSp[fileSp.length - 1].toLowerCase();
    if (allowedExtension.indexOf(fileEx) >= 0) {
        return true;
    }

    return false;
};


var filterFiles = function (files) {
    var nFiles = [];
    for (var i = 0; i < files.length; i += 1) {
        if (checkFileExt(files[i].name)) {
            nFiles.push(files[i])
        }
    }
    return nFiles
};

var selectedFile = null;

var resetSelectedFile = function () {
    $('.selected-file-area').hide();
    $('.selected-file-area .filename').text('');
    selectedFile = null;
};

var setSelectedFile = function (file) {
    $('.selected-file-area').show();
    $('.selected-file-area .filename').text(file.name);
    selectedFile = file;
};


$('.upload-area').on({
    dragover: function (evt) {
        evt.preventDefault();
    },
    drop: function (evt) {
        evt.preventDefault();
        var files = evt.originalEvent.dataTransfer.files;
        var filteredFiles = filterFiles(files);
        if (filteredFiles.length > 0) {
            setSelectedFile(filteredFiles[0]);
        } else {
            resetSelectedFile();
        }
    }
});


$('#the-file').change(function (e) {
    var files = e.target.files;
    resetSelectedFile();
    var filteredFiles = filterFiles(files);
    if (filteredFiles.length > 0) {
        setSelectedFile(filteredFiles[0]);
    } else {
        resetSelectedFile();
    }
});

$('.upload-area').click(function () {
    $('#the-file').trigger('click');
});

$('.btn-next').click(function () {
    if (selectedFile !== null) {
        var reader = new FileReader();

        reader.addEventListener('load', function () {
            submit(reader.result)
        });

        reader.readAsDataURL(selectedFile);
    }
});

var submit = function (fileContents) {
    $('.btn-next').prop('disabled', true);
    $('input[name="file"]').val(fileContents);
    $('.upload-form').submit();
};