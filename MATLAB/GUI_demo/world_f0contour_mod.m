function varargout = world_f0contour_mod(varargin)
% WORLD_F0CONTOUR_MOD MATLAB code for world_f0contour_mod.fig
%      WORLD_F0CONTOUR_MOD, by itself, creates a new WORLD_F0CONTOUR_MOD or raises the existing
%      singleton*.
%
%      H = WORLD_F0CONTOUR_MOD returns the handle to a new WORLD_F0CONTOUR_MOD or the handle to
%      the existing singleton*.
%
%      WORLD_F0CONTOUR_MOD('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in WORLD_F0CONTOUR_MOD.M with the given input arguments.
%
%      WORLD_F0CONTOUR_MOD('Property','Value',...) creates a new WORLD_F0CONTOUR_MOD or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before world_f0contour_mod_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to world_f0contour_mod_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help world_f0contour_mod

% Last Modified by GUIDE v2.5 19-Sep-2017 12:42:18

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @world_f0contour_mod_OpeningFcn, ...
                   'gui_OutputFcn',  @world_f0contour_mod_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before world_f0contour_mod is made visible.
function world_f0contour_mod_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to world_f0contour_mod (see VARARGIN)

% Choose default command line output for world_f0contour_mod
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes world_f0contour_mod wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = world_f0contour_mod_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;



function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global_data= getappdata(0,'WAV_DATA');
play(global_data.player);



% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs= global_data.fs;
inc_value= str2double(get(handles.edit1,'string'));
disp(inc_value);
f0_parameter = Harvest(x, fs);
f0_parameter.f0 = f0_parameter.f0+((inc_value/100)*f0_parameter.f0);
spectrum_parameter = CheapTrick(x, fs, f0_parameter);
source_parameter = D4C(x, fs, f0_parameter);
y = Synthesis(source_parameter, spectrum_parameter);
disp('done');
handles.player = audioplayer(y,fs);
handles.y=y;
handles.output = hObject;
guidata(hObject, handles);


%PLAYER --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
play(handles.player);


% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
figure();
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs= global_data.fs;
subplot(2,1,1);
plot(0:1/fs: (length(x)-1)/fs,x);
title('Waveform')
xlabel('Time(s)');ylabel('Amplitude');
subplot(2,1,2);
plot(0:1/fs: (length(handles.y)-1)/fs,handles.y);%x axis should be [1:round(length(x)/length(source_parameter.f0)):length(y)]
title('Modified Sound Waveform')
xlabel('Time(s)');ylabel('Amplitude');
