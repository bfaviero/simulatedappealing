#include "webcam.hpp"

using namespace cv;
using namespace std;

Mat ellipticKernel(int width, int height = -1) {
 if (height==-1) {
  return getStructuringElement(MORPH_ELLIPSE,Size(width,width), Point(width/2, width/2));
 } else {
  return getStructuringElement(MORPH_ELLIPSE,Size(width,height), Point(width/2, height/2));
 }
}

float[] whiteboardToImage(float[] whiteboard_point) {
 return whiteboard_point;
}

float[] imageToWhiteboard(float[] image_point) {
 return whiteboard_point;
}

int main (int argc, char** argv) {

/*****
 begin camera setup
*****/

 CvCapture* capture = 0;
 int width, height;

 capture = cvCaptureFromCAM(0);

 if (!capture) {
  printf("No camera detected!");
  return -1;
 }

 ifstream config_file (".config");

 if (config_file.is_open()) {
// does not support corrupted .config

  string line;
  getline(config_file, line);
  istringstream(line)>>width;
  getline(config_file, line);
  istringstream(line)>>height;
  cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, width);
  cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, height);

  config_file.close();

 } else {

  initResolutions();

  for (int i=36; i<150; i++) {
   cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH, resolutions[i].width);
   cvSetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT, resolutions[i].height);
  }

  width = cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_WIDTH);
  height = cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_HEIGHT);

  ofstream config_file_out(".config");
  config_file_out << width;
  config_file_out << "\n";
  config_file_out << height;
  config_file_out << "\n";
  config_file_out.close();
 }

 for (int i = 0; i < 15; i++) {
  // capture some frames so exposure correction takes place
  cvQueryFrame(capture);
 }

/*****
 end camera setup
*****/

 int tracker1, tracker2, tracker3, tracker4;
 namedWindow("settings",1);
 createTrackbar("1","settings",&tracker1,100);
 createTrackbar("2","settings",&tracker2,100);
 createTrackbar("3","settings",&tracker3,100);
 createTrackbar("4","settings",&tracker4,100);

 bool keep_going = true;

 while (keep_going) {

  Mat image(cvQueryFrame(capture));
//  imshow("webcam", image);


 }

 cvReleaseCapture(&capture);

 return 0;
}

