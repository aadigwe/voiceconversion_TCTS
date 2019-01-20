%%%%%%CALLING PYTHON FUNCTIONS %%%%%%%%%%%%%%%%%

function varargout = world_parameter(varargin)
% WORLD_PARAMETER MATLAB code for world_parameter.fig
%      WORLD_PARAMETER, by itself, creates a new WORLD_PARAMETER or raises the existing
%      singleton*.
%
%      H = WORLD_PARAMETER returns the handle to a new WORLD_PARAMETER or the handle to
%      the existing singleton*.
%
%      WORLD_PARAMETER('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in WORLD_PARAMETER.M with the given input arguments.
%
%      WORLD_PARAMETER('Property','Value',...) creates a new WORLD_PARAMETER or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before world_parameter_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to world_parameter_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help world_parameter

% Last Modified by GUIDE v2.5 04-Oct-2017 13:52:49

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @world_parameter_OpeningFcn, ...
                   'gui_OutputFcn',  @world_parameter_OutputFcn, ...
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


% --- Executes just before world_parameter is made visible.
function world_parameter_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to world_parameter (see VARARGIN)

% Choose default command line output for world_parameter
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes world_parameter wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = world_parameter_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

%OPEN FILE BUTTON
% --- Executes on button press in pushbutton13.
function pushbutton13_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%ADD SUBFOLDERS DIRECTORY
addpath(genpath('World_functions'))
addpath(genpath('Speech_files'))
addpath(genpath('GUI_demo'))
addpath(genpath('Other_dependencies'))
addpath(genpath('Formant_shifts'))

[filename,pathname]=uigetfile({'*.*';'*.wav'},'????');
if isequal(filename,0)||isequal(pathname,0)
  errordlg('Choose nothing','Error');%
  return;
else
    audio_original=[pathname,filename];%
    filename_save=filename;
    audio_save=audio_original;
    [x, fs] = audioread(filename);
    disp(filename);
    disp(fs);
    f0_parameter = Harvest(x, fs);
    handles.current_data =x;
    handles.fs= fs;
    handles.output = hObject;
    handles.player = audioplayer(handles.current_data,handles.fs);
    set(handles.text5,'String',[filename]);
    guidata(hObject, handles);
    global_data.wav=x;
    global_data.fs=fs;
    global_data.filename=filename;
    global_data.f0_parameter=f0_parameter;
    global_data.player=handles.player;
    setappdata(0,'WAV_DATA',global_data);
end


% --- Executes on button press in pushbutton14.
function pushbutton14_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
play(handles.player);


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


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton11.
function pushbutton11_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%FORMANTS DETECTION GUI
% --- Executes on button press in pushbutton12.
function pushbutton12_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
formant_estimation_GUI25


%PITCH PARAMETER CONTROL
% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
world_f0contour_mod

%FORMANT CONTROL
% --- Executes on button press in pushbutton8.
function pushbutton8_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton8 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
world_fomant_version1


% --- Executes on button press in pushbutton9.
function pushbutton9_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton9 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton10.
function pushbutton10_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
 handles = guidata(hObject);
 x=handles.current_data;
 fs= handles.fs;
 if 0 
  f0_parameter = Dio(x, fs);
  f0_parameter.f0 = StoneMask(x, fs,...
    f0_parameter.temporal_positions, f0_parameter.f0);
end;
f0_parameter = Harvest(x, fs);
figure();
subplot(2,1,1);
plot(0:1/fs: (length(x)-1)/fs,x);
title('Waveform')
xlabel('Time(s)');ylabel('Amplitude');
subplot(2,1,2);
plot([0:(length(x)/length(f0_parameter.f0)):(length(x)-1)]/fs,f0_parameter.f0);%x axis should be [1:round(length(x)/length(source_parameter.f0)):length(y)]
title('Pitch contour')
xlabel('Time(s)');ylabel('Pitch');
handles.f0 =f0_parameter;
handles.output = hObject;
guidata(hObject, handles);


%SPECTRAL ENVELOPE ANALYSIS
% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles = guidata(hObject);
x=handles.current_data;
fs=handles.fs;
f0_parameter=handles.f0;
spectrum_parameter = CheapTrick(x, fs, f0_parameter);
HMobj=HeatMap(spectrum_parameter.spectrogram,'Colormap',parula, 'Standardize',2, 'DisplayRange', 1);
%HMobj=HeatMap(spectrum_parameter.spectrogram.','Colormap',parula, 'Standardize',2, 'DisplayRange', 1, 'ColumnLabels',[1:1:513]);
addTitle (HMobj,'Spectrogram of Audio File using spectral values')
addXLabel(HMobj, 'Time (s)', 'FontSize', 12)
addYLabel(HMobj, 'Frequency (Hz)', 'FontSize', 12)
handles.spectrum =spectrum_parameter;
handles.output = hObject;
guidata(hObject, handles);

%APERIODICITY ANALYSIS
% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles = guidata(hObject);
x=handles.current_data;
fs=handles.fs;
f0_parameter=handles.f0;
spectrum_parameter=handles.spectrum;
source_parameter = D4C(x, fs, f0_parameter);
HM2obj=HeatMap(source_parameter.aperiodicity,'Colormap',parula, 'Standardize',1.5, 'DisplayRange', 1);
addTitle (HM2obj,'Aperiodicity')
addXLabel(HM2obj, 'Time (s)', 'FontSize', 12)
addYLabel(HM2obj, 'Frequency (Hz)', 'FontSize', 12)
handles.spectrum =spectrum_parameter;
handles.output = hObject;
guidata(hObject, handles);

%SPECTRAL FRAME ANALYSIS
% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
world_spectral_env;
%handles = guidata(hObject);
%x=handles.current_data;
%fs=handles.fs;
%f0_parameter=handles.f0;
%cheap_trick2(x, fs, f0_parameter);



% --- If Enable == 'on', executes on mouse press in 5 pixel border.
% --- Otherwise, executes on mouse press in 5 pixel border or over text5.
function text5_ButtonDownFcn(hObject, eventdata, handles)
% hObject    handle to text5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in pushbutton15.
function pushbutton15_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

%SHIFT WHOLEWAVEFORM 
% --- Executes on button press in pushbutton16.
function pushbutton16_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton16 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
world_formant_shift_version2

%VOWEL CONVERSION
% --- Executes on button press in pushbutton17.
function pushbutton17_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
vowel_conversion
