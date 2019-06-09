$body = $("body");

var generalCourses = [];
var coreCourses = [];
var electiveCourses = [];

var selectedCourses = [];

var response = null;

function renderRecommendedCourses(resp) {
    $('#studentInfo').css('display', 'block');
    $('#gpa').text(resp['StudentData']['GPA']);
    $('#credit').text(`${resp['StudentData']['Credits']} Credits`);
    let predictedGrades = resp['PredictedData'];

    if (predictedGrades['General'].length > 0) {
        generalCourses = sortList(predictedGrades['General'], 'PredictedGrade', false);
        $('#generalCourses').empty();
        $.each(generalCourses, function (index, value) {
            // console.log(value);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: "btn btn-primary",
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#generalCourses').append(r);
        });
    }

    if (predictedGrades['Core'].length > 0) {
        coreCourses = sortList(predictedGrades['Core'], 'PredictedGrade', false);
        $('#coreCourses').empty();
        $.each(coreCourses, function (index, value) {
            // console.log(value);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: "btn btn-warning",
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#coreCourses').append(r);
        });
    }

    if (predictedGrades['Elective'].length > 0) {
        electiveCourses = sortList(predictedGrades['Elective'], 'PredictedGrade', false);
        $('#electiveCourses').empty();
        $.each(electiveCourses, function (index, value) {
            // console.log(value);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: "btn btn-success",
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#electiveCourses').append(r);
        });
    }
}

function refreshRecommendedCourse() {
    // console.log('refresh')
    if (generalCourses.length > 0) {
        $('#generalCourses').empty();
        // console.log(generalCourses)
        $.each(generalCourses, function (index, value) {
            // console.log(value);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: "btn btn-primary",
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#generalCourses').append(r);
        });
    } else {
        $('#generalCourses').empty().append('N/A');
    }

    if (coreCourses.length > 0) {
        $('#coreCourses').empty();
        $.each(coreCourses, function (index, value) {
            // console.log(value);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: "btn btn-warning",
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#coreCourses').append(r);
        });
    } else {
        $('#coreCourses').empty().append('N/A');
    }

    if (electiveCourses.length > 0) {
        $('#electiveCourses').empty();
        $.each(electiveCourses, function (index, value) {
            // console.log(value);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: "btn btn-success",
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#electiveCourses').append(r);
        });
    } else {
        $('#electiveCourses').empty().append('N/A');
    }

}

function refreshSelectedCourses() {
    if (selectedCourses.length > 0) {
        let totalCredits = 0;
        let sumGrades = 0;
        $('#selectedCourse').empty();
        $.each(selectedCourses, function (index, value) {
            totalCredits += parseInt(value['Credit']);
            sumGrades += (getGPAToEstimate(value['PredictedGrade']) * parseFloat(value['Credit']));
            // console.log(value['CourseCode']);
            let r = $('<input/>').attr({
                type: "button",
                id: value['CourseCode'],
                value: value['CourseName'],
                class: value['Class'],
                style: "margin: 8px",
                onclick: `openDialog('${value['CourseCode']}','${value['CourseName']}','${value['RequiredGrade']}','${value['PredictedGrade']}','${value['ActualGrade']}','${value['Credit']}')`
            });

            $('#selectedCourse').append(r).append('<br>');
        });
        $('#totalCredits').text(`Total Credits: ${totalCredits}`)
        $('#predictedGPA').text(`Predicted GPA: ${(sumGrades / totalCredits).toFixed(2)}`);
        $('#actualGPA').text(`Actual GPA: ${calculateActualGPA(selectedCourses)}`)
    } else {
        $('#selectedCourse').empty();
        $('#totalCredits').empty();
        $('#predictedGPA').empty();
        $('#actualGPA').empty();
    }
}

function openDialog(courseCode, courseName, requiredGrade, predictedGrade, actualGrade, credit) {
    Swal.fire({
        title: '<strong>Course Information</strong>',
        type: 'info',
        width: '400px',
        animated: false,
        html:
            '<div style="text-align: left">' +
            '<b>Course Code:</b> ' + courseCode + ' <br>' +
            '<b>Course Name:</b> ' + courseName + ' <br>' +
            '<b>Credit:</b> ' + credit + ' <br>' +
            '<b>Required Grade:</b> ' + requiredGrade + ' <br>' +
            '<b>Predicted Grade:</b> ' + predictedGrade + ' <br>' +
            '<b>Actual Grade:</b> ' + actualGradeToString(actualGrade) + ' <br>' +
            '</div>',
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Add',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.value) {
            if (generalCourses.length > 0) {
                $.each(generalCourses, function (generalIndex, generalValue) {
                    if (generalValue !== undefined) {
                        if (courseCode === generalValue['CourseCode']) {
                            let course = {
                                'CourseCode': courseCode,
                                'CourseName': courseName,
                                'RequiredGrade': requiredGrade,
                                'PredictedGrade': predictedGrade,
                                'ActualGrade': actualGrade,
                                'Credit': credit,
                                'Type': 'General',
                                'Class': 'btn btn-primary'
                            };
                            selectedCourses.push(course);
                            // console.log(generalIndex);
                            generalCourses.splice(generalIndex, 1)
                        }
                    }
                });
            }

            if (coreCourses.length > 0) {
                $.each(coreCourses, function (coreIndex, coreValue) {
                    if (coreValue !== undefined) {
                        if (courseCode === coreValue['CourseCode']) {
                            let course = {
                                'CourseCode': courseCode,
                                'CourseName': courseName,
                                'RequiredGrade': requiredGrade,
                                'PredictedGrade': predictedGrade,
                                'ActualGrade': actualGrade,
                                'Credit': credit,
                                'Type': 'Core',
                                'Class': 'btn btn-warning'
                            };
                            selectedCourses.push(course);
                            // console.log('found');
                            coreCourses.splice(coreIndex, 1)
                        }
                    }
                });
            }

            if (electiveCourses.length > 0) {
                $.each(electiveCourses, function (electiveIndex, electiveValue) {
                    if (electiveValue !== undefined) {
                        if (courseCode === electiveValue['CourseCode']) {
                            let course = {
                                'CourseCode': courseCode,
                                'CourseName': courseName,
                                'RequiredGrade': requiredGrade,
                                'PredictedGrade': predictedGrade,
                                'ActualGrade': actualGrade,
                                'Credit': credit,
                                'Type': 'Elective',
                                'Class': 'btn btn-success'
                            };
                            selectedCourses.push(course);
                            // console.log('found');
                            electiveCourses.splice(electiveIndex, 1)
                        }
                    }
                });
            }

            refreshRecommendedCourse();
            refreshSelectedCourses();
        }
    })
}

function sortList(list, prop, asc) {
    list = list.sort(function (a, b) {
        if (asc) {
            return (a[prop] > b[prop]) ? 1 : ((a[prop] < b[prop]) ? -1 : 0);
        } else {
            return (b[prop] > a[prop]) ? 1 : ((b[prop] < a[prop]) ? -1 : 0);
        }
    });
    return list;
}

function actualGradeToString(grade) {
    if (grade === -1 || grade === '-1') {
        return 'N/A'
    } else if (grade === 4 || grade === '4') {
        return '4.00'
    }
    return grade
}

function calculateActualGPA(courses) {
    var notAvailable = false;
    if (courses.length > 0) {
        let totalCredits = 0;
        let sumGrades = 0;
        $.each(selectedCourses, function (index, value) {
            // console.log(parseFloat(value['ActualGrade']))
            if (parseFloat(value['ActualGrade']) >= 0) {
                // console.log('yes')
                totalCredits += parseInt(value['Credit']);
                sumGrades += (getGPAToEstimate(value['ActualGrade']) * parseFloat(value['Credit']));
            } else {
                notAvailable = true
            }
        });
        if (notAvailable) {
            return 'Not Available'
        } else {
            return (sumGrades / totalCredits).toFixed(2)
        }
    }
}

$(document).on({
    ajaxStart: function () {
        $('#loader').css('display', 'block');
        $('#predictedCorusesParent').css('display', 'none');
    },
    ajaxStop: function () {
        $('#loader').css('display', 'none');
        $('#predictedCorusesParent').css('display', 'block');
        renderTable();
        setupSelectedCourseTable();
    }
});

$(document).ready(function () {
    $('#submitId').click(function () {
        var studentId = $('#studentId').val();

        generalCourses.length = 0;
        coreCourses.length = 0;
        electiveCourses.length = 0;
        selectedCourses.length = 0;

        refreshSelectedCourses();
        refreshRecommendedCourse();

        $.ajax({
            url: "/student",
            type: "POST",
            data: studentId,
            contentType: 'json',
            dataType: 'json',
            success: function (resp) {
                response = resp;
                renderRecommendedCourses(resp);
            },
            error: function (error) {
                alert(error);
            }
        });
    });
});

