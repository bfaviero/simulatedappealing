
#include "webcam.hpp"

using namespace cv;
using namespace std;

Mat image_wb_map_x, image_wb_map_y;
bool madeMaps = false;

Mat extractBoundingBox(Mat whiteboard, Rect bounding_box) {
 return whiteboard(bounding_box);
}

Mat ellipticKernel(int width, int height = -1) {
 if (height==-1) {
  return getStructuringElement(MORPH_ELLIPSE,Size(width,width), Point(width/2, width/2));
 } else {
  return getStructuringElement(MORPH_ELLIPSE,Size(width,height), Point(width/2, height/2));
 }
}

void createMaps() {
 image_wb_map_x.create(Size(1200,800), CV_32FC1);
 image_wb_map_y.create(Size(1200,800), CV_32FC1);
 Mat dummy_x, dummy_y;
 dummy_x.create(Size(1280,720), CV_32FC1);
 dummy_y.create(Size(1280,720), CV_32FC1);
 for (int j = 0; j < 720; j++) {
  for (int i = 0; i < 1280; i++) {
   dummy_x.at<float>(j,i) = i;
   dummy_y.at<float>(j,i) = j;
  }
 }
 Point2f source_points[4];
 Point2f dest_points[4];
 // TODO: calculate from threshold and hough transform
 source_points[0] = Point2f(456-225,236-124);
 source_points[1] = Point2f(1268-225,207-124);
 source_points[2] = Point2f(481-225,764-124);
 source_points[3] = Point2f(1230-225,763-124);

 dest_points[0] = Point2f(0,0);
 dest_points[1] = Point2f(1200,0);
 dest_points[2] = Point2f(0,800);
 dest_points[3] = Point2f(1200,800);

 Mat transform_matrix = getPerspectiveTransform(source_points, dest_points);
 warpPerspective(dummy_x, image_wb_map_x, transform_matrix, Size(1200,800));
 warpPerspective(dummy_y, image_wb_map_y, transform_matrix, Size(1200,800));
 madeMaps = true;
}

Mat webcamToWhiteboard(Mat frame) {
 if (!madeMaps) {
  createMaps();
 }
 Mat whiteboard;
 whiteboard.create(Size(1200, 800), frame.type());
 remap(frame, whiteboard, image_wb_map_x, image_wb_map_y, CV_INTER_LINEAR);
 return whiteboard;
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

  string filename = "";
  string identifier = "";
  while (filename.compare("") == 0) {
   DIR* dir = opendir(".");
   struct dirent *de;
   while (dir) {
    de = readdir(dir);
    if (!de) break;
    filename = de->d_name;
    if (filename.find("_bounding") < filename.length()) {
     identifier = "";
     for (int q=0;q<filename.length();q++) {
      if (filename[q]!='_') {
       identifier+=filename[q];
      } else {
       break;
      }
     }
     break;
    } else {
     filename = "";
    }
   }
  }

  // open and parse filename
  ifstream bounding_file (filename.c_str());
  vector<Rect> bounding_boxes;
  while (bounding_file.good()) {
   string line;
   getline(bounding_file, line);
   istringstream iss(line);
   vector<string> coords = vector<string>(istream_iterator<string>(iss), istream_iterator<string>());
   int x1, y1, x2, y2;
   if (coords.size() != 4) {
    continue;
   }
   istringstream(coords[0]) >> x1;
   istringstream(coords[1]) >> y1;
   istringstream(coords[2]) >> x2;
   istringstream(coords[3]) >> y2;
   Rect box(x1,y1,x2-x1,y2-y1);
   bounding_boxes.push_back(box);
  }
  Mat initial_frame(cvQueryFrame(capture));
  Mat initial_whiteboard = webcamToWhiteboard(initial_frame);
  vector<Mat> bounding_box_buffers;
  vector<Mat> initial_buffers;
  for (int i = 0; i < bounding_boxes.size(); i++) {
   Mat bounding_box_buffer = initial_whiteboard(bounding_boxes[i]);
   Mat other;
   GaussianBlur(bounding_box_buffer, other, Size(5,5), 0, 0);
   initial_buffers.push_back(other);
   bounding_box_buffers.push_back(other);
  }

  bool detecting = true;
  vector<int> states;
  for (int j=0; j<bounding_boxes.size(); j++) {
   states.push_back(0);
  }
  while (detecting) {
   Mat image(cvQueryFrame(capture));
   Mat whiteboard = webcamToWhiteboard(image);
Mat whiteboard_rects(whiteboard);
imshow("whiteboard", whiteboard_rects);
   int box = -1;
//int loaep = bounding_boxes.size();
//printf("%d\n", loaep);
   for (int i=0; i<bounding_boxes.size(); i++) {
    Mat bounding_box_image = whiteboard(bounding_boxes[i]);
    Mat blurred;
    GaussianBlur(bounding_box_image, blurred, Size(5,5), 0, 0);
    Mat flow_image = abs(bounding_box_image - bounding_box_buffers[i]);
    Mat grayscale_flow;
    cvtColor(flow_image, grayscale_flow, CV_BGR2GRAY);
    threshold(grayscale_flow, grayscale_flow, 20, 0, 3);
    if (mean(grayscale_flow)[0]<10.0) {
     bounding_box_buffers[i] = bounding_box_buffers[i]*0.5 + blurred*0.5;
    }
if (states[i] == 0 && mean(grayscale_flow)[0]>15.0) {
states[i] = 1;
}
if (states[i] == 1 && mean(grayscale_flow)[0] < 10.0) {
states[i] = 2;
}
if (states[i] > 1) {
states[i] += 1;
}
if (states[i] > 8) {
Mat processed;
cvtColor(whiteboard(bounding_boxes[i]), processed, CV_BGR2GRAY);
threshold(processed, processed, 60, 255, 3);
// threshold_2 OCR PREPROCESS
threshold(processed, processed, 150, 255, 0);
// threshold_1 OCR PREPROCESS
morphologyEx(processed, processed, MORPH_OPEN, ellipticKernel(20));
// dilate size OCR PREPROCESS
if (mean(processed)[0]<250) {
box = i;
} else {
states[i]++;
if (states[i] > 12) {
states[i] = 0;
}
}
//box = i;
}
   }

   // TODO: write code to figure out when a box has been filled in
   // try to see if the person finished writing something in each bounding box
   // ideas:
   // - white border means no hand
   // - movement means something is being written to there
   // - movement then no movement means something was written, iff no hand in frame
   // - morphological operation and weight of marker can tell if hand is in image
   // box == -1 -> nothing detected; else box==id -> id detected

   if (box != -1) {
    Mat handwriting = extractBoundingBox(whiteboard, bounding_boxes.at(box));

    Mat processed;
    cvtColor(handwriting, processed, CV_BGR2GRAY);

    char buf[100];
    sprintf(buf, "%d", box);
    string buf_s = string(buf);
    imwrite(identifier+"_"+buf_s+"_bounding.jpg", processed);
threshold(processed, processed, 70, 255, 3);
// threshold_2 OCR PREPROCESS
threshold(processed, processed, 140, 255, 0);
// threshold_1 OCR PREPROCESS
morphologyEx(processed, processed, MORPH_OPEN, ellipticKernel(6));
// dilate size OCR PREPROCESS
//    imshow("HANDWRITING",processed);
    detecting = false;
    return 0;
   }
   waitKey(1);
  }

 }

 cvReleaseCapture(&capture);

 return 0;
}

