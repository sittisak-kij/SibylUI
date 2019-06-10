function getGPAToEstimate(gpa) {
    gpa = parseFloat(gpa);
    if (gpa <= 0) {
        return 0
    } else if (gpa >= 1 && gpa <= 1.49) {
        return 1
    } else if (gpa >= 1.50 && gpa <= 1.99) {
        return 1.75
    } else if (gpa >= 2.00 && gpa <= 2.14) {
        return 2.00
    } else if (gpa >= 2.15 && gpa <= 2.49) {
        return 2.15
    } else if (gpa >= 2.50 && gpa <= 2.75) {
        return 2.75
    } else if (gpa >= 2.76 && gpa <= 3.14) {
        return 3.00
    } else if (gpa >= 3.15 && gpa <= 3.49) {
        return 3.15
    } else if (gpa >= 3.50 && gpa <= 3.75) {
        return 3.75
    } else {
        return 4.00
    }
}

function roundCeil(gpa) {
    gpa = parseFloat(gpa);
    if (gpa <= 0) {
        return 0
    } else if (gpa >= 0.01 && gpa <= 1.00) {
        return 1
    } else if (gpa >= 1.01 && gpa <= 1.75) {
        return 1.75
    } else if (gpa >= 1.76 && gpa <= 2.00) {
        return 2.00
    } else if (gpa >= 2.01 && gpa <= 2.25) {
        return 2.15
    } else if (gpa >= 2.26 && gpa <= 2.75) {
        return 2.75
    } else if (gpa >= 2.76 && gpa <= 3.00) {
        return 3.00
    } else if (gpa >= 3.01 && gpa <= 3.25) {
        return 3.15
    } else if (gpa >= 3.26 && gpa <= 3.75) {
        return 3.75
    } else {
        return 4.00
    }
}

function roundFloor(gpa) {
    gpa = parseFloat(gpa);
    if (gpa <= 0 && gpa <= 0.99) {
        return 0
    } else if (gpa >= 1.00 && gpa <= 1.74) {
        return 1
    } else if (gpa >= 1.75 && gpa <= 1.99) {
        return 1.75
    } else if (gpa >= 2.00 && gpa <= 2.24) {
        return 2.00
    } else if (gpa >= 2.25 && gpa <= 2.74) {
        return 2.15
    } else if (gpa >= 2.75 && gpa <= 2.99) {
        return 2.75
    } else if (gpa >= 3.00 && gpa <= 3.24) {
        return 3.00
    } else if (gpa >= 3.25 && gpa <= 3.74) {
        return 3.15
    } else if (gpa >= 3.75 && gpa <= 3.99) {
        return 3.75
    } else {
        return 4.00
    }
}

function roundMidrange(gpa) {
    gpa = parseFloat(gpa);
    if (gpa <= 0 && gpa <= 0.50) {
        return 0
    } else if (gpa >= 0.51 && gpa <= 1.375) {
        return 1
    } else if (gpa >= 1.376 && gpa <= 1.875) {
        return 1.75
    } else if (gpa >= 1.876 && gpa <= 2.215) {
        return 2.00
    } else if (gpa >= 2.126 && gpa <= 2.50) {
        return 2.15
    } else if (gpa >= 2.51 && gpa <= 2.875) {
        return 2.75
    } else if (gpa >= 2.876 && gpa <= 3.125) {
        return 3.00
    } else if (gpa >= 3.126 && gpa <= 3.50) {
        return 3.15
    } else if (gpa >= 3.51 && gpa <= 3.875) {
        return 3.75
    } else {
        return 4.00
    }
}