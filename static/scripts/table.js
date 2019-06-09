var newSelectedCourses = [];

function renderTable() {
    let table = $('#recommendedCoursesTable').DataTable({
        bLengthChange: false,
        scrollY: '410px',
        searching: false,
        bInfo: false,
        columnDefs: [{
            targets: 0,
            className: 'text-center'
        }, {
            targets: 2,
            className: 'text-center'
        }, {
            targets: 3,
            className: 'text-center'
        }, {
            targets: 4,
            className: 'text-center'
        }, {
            targets: 5,
            className: 'text-center'
        }]
    });

    $('#recommendedCoursesTable tbody').on('click', 'tr', function () {
        let data = table.row(this).data();
        newSelectedCourses.push(data);
        updateSelectedCourseTable();
    });

    table.clear();

    let recommendedCourses = response['PredictedData'];
    $.each(recommendedCourses, function (i, value) {
        $.each(value, function (j, courseData) {
            let data = [];
            data.push(courseData['CourseCode']);
            data.push(courseData['CourseName']);
            data.push(courseData['Credit']);
            data.push(courseData['Type']);
            data.push(courseData['PredictedGrade']);
            data.push(actualGradeToString(courseData['ActualGrade']));
            table.row.add(data).draw();
        });
    });
    table.columns.adjust().order([[5, 'desc'], [4, 'desc']]).draw();
}

function setupSelectedCourseTable() {
    $('#selectedCoursesTable').DataTable({
        bLengthChange: false,
        scrollY: '230px',
        searching: false,
        bInfo: false,
        paging: false,
        columnDefs: [{
            targets: 0,
            className: 'text-center'
        }, {
            targets: 2,
            className: 'text-center'
        }, {
            targets: 3,
            className: 'text-center'
        }, {
            targets: 4,
            className: 'text-center'
        }, {
            targets: 5,
            className: 'text-center'
        }],
        language: {
            emptyTable: 'No selected course(s)'
        }
    });
}

function updateSelectedCourseTable() {
    let table = $('#selectedCoursesTable').DataTable();

    table.clear();
    let totalCredits = 0;
    let predictedGPAs = [0.0, 0.0, 0.0];
    $.each(newSelectedCourses, function (i, value) {
        table.row.add(value).draw();
        totalCredits += parseInt(value[2]);
        // console.log(`Ceil: ${roundCeil(value[4])} | Floor ${roundFloor(value[4])} | Mid-range ${roundMidrange(value[4])}`)
        predictedGPAs[0] += roundCeil(value[4]) * parseFloat(value[2]);
        predictedGPAs[1] += roundFloor(value[4]) * parseFloat(value[2]);
        predictedGPAs[2] += roundMidrange(value[4]) * parseFloat(value[2]);
    });
    table.columns.adjust().order([[5, 'desc'], [4, 'desc']]).draw();

    $('#tCredits').text(`${totalCredits} Credits`);
    $('#nActualGPA').text(checkNaN(calculateActualGPA2()));
    $('#ceil').text(checkNaN((predictedGPAs[0] / totalCredits).toFixed(2)));
    $('#floor').text(checkNaN((predictedGPAs[1] / totalCredits).toFixed(2)));
    $('#mid-range').text(checkNaN((predictedGPAs[2] / totalCredits).toFixed(2)));

    $('#selectedCoursesTable tbody').on('click', ' tr', function () {
        let data = table.row(this).data();
        table.row(this).remove().draw();
        let index = newSelectedCourses.indexOf(data[0]);
        newSelectedCourses.splice(index, 1);
        updateSelectedCourseTable()
    });
}

function calculateActualGPA2() {
    let notAvailable = false;
    let totalCredits = 0;
    let sumGrades = 0;
    if (newSelectedCourses.length > 0) {
        $.each(newSelectedCourses, function (index, value) {
            if (isNaN(parseFloat(value[5]))) {
                notAvailable = true;
            } else {
                totalCredits += parseInt(value[2]);
                sumGrades += parseFloat(value[5]) * parseFloat(value[2]);
            }
        })
    }
    if (notAvailable) {
        return 'Not Available'
    } else {
        return (sumGrades / totalCredits).toFixed(2)
    }
}

function checkNaN(value) {
    if (isNaN(value)) {
        return 'Not Available'
    } else {
        return value
    }
}