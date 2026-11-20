import static org.hamcrest.Matchers.equalTo;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;

import io.restassured.RestAssured;
import static io.restassured.RestAssured.given;
import static io.restassured.RestAssured.post;
import static io.restassured.RestAssured.when;
import io.restassured.http.ContentType;

@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
public class AttendanceApiTest {

    @BeforeAll
    public static void setup() {
        RestAssured.baseURI = "http://127.0.0.1:5000";
        post("/api/reset").then().statusCode(200);
    }

    @Test
    @Order(1)
    public void testMarkValidAttendanceApi() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"student_id\": \"102\"}")
        .when()
            .post("/api/attendance")
        .then()
            .statusCode(201)
            .body("message", equalTo("Attendance marked"))
            .body("record.name", equalTo("Divya"));
    }

    @Test
    @Order(2)
    public void testDuplicateAttendanceApiReturns400() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"student_id\": \"102\"}")
        .when()
            .post("/api/attendance")
        .then()
            .statusCode(400)
            .body("error", equalTo("Duplicate attendance entry"));
    }

    @Test
    @Order(3)
    public void testInvalidStudentIdApiReturns404() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"student_id\": \"999\"}")
        .when()
            .post("/api/attendance")
        .then()
            .statusCode(404)
            .body("error", equalTo("Invalid Student ID"));
    }

    @Test
    @Order(4)
    public void testGetAttendanceSummaryApi() {
        when()
            .get("/api/attendance")
        .then()
            .statusCode(200)
            .body("total", equalTo(1))
            .body("records[0].student_id", equalTo("102"));
    }

    @Test
    @Order(5)
    public void testBlankStudentIdApiReturns400() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"student_id\": \"   \"}")
        .when()
            .post("/api/attendance")
        .then()
            .statusCode(400)
            .body("error", equalTo("Student ID is required"));
    }

    @Test
    
    @Order(6)
    public void testMarkSecondStudentAndVerifyTotalApi() {
        given()
            .contentType(ContentType.JSON)
            .body("{\"student_id\": \"103\"}")
        .when()
            .post("/api/attendance")
        .then()
            .statusCode(201)
            .body("record.name", equalTo("Rohan"));

        when()
            .get("/api/attendance")
        .then()
            .statusCode(200)
            .body("total", equalTo(2));
    }
}