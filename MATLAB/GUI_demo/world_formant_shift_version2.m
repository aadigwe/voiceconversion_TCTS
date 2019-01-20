function varargout = world_formant_shift_version2(varargin)
% WORLD_FORMANT_SHIFT_VERSION2 MATLAB code for world_formant_shift_version2.fig
%      WORLD_FORMANT_SHIFT_VERSION2, by itself, creates a new WORLD_FORMANT_SHIFT_VERSION2 or raises the existing
%      singleton*.
%
%      H = WORLD_FORMANT_SHIFT_VERSION2 returns the handle to a new WORLD_FORMANT_SHIFT_VERSION2 or the handle to
%      the existing singleton*.
%
%      WORLD_FORMANT_SHIFT_VERSION2('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in WORLD_FORMANT_SHIFT_VERSION2.M with the given input arguments.
%
%      WORLD_FORMANT_SHIFT_VERSION2('Property','Value',...) creates a new WORLD_FORMANT_SHIFT_VERSION2 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before world_formant_shift_version2_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to world_formant_shift_version2_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help world_formant_shift_version2

% Last Modified by GUIDE v2.5 04-Oct-2017 11:06:56

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @world_formant_shift_version2_OpeningFcn, ...
                   'gui_OutputFcn',  @world_formant_shift_version2_OutputFcn, ...
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


% --- Executes just before world_formant_shift_version2 is made visible.
function world_formant_shift_version2_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to world_formant_shift_version2 (see VARARGIN)

% Choose default command line output for world_formant_shift_version2
handles.output = hObject;
global_data= getappdata(0,'WAV_DATA');
disp(global_data)

set(handles.text3,'String',['Filename: ',global_data.filename]);
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes world_formant_shift_version2 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = world_formant_shift_version2_OutputFcn(hObject, eventdata, handles) 
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



function edit2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2 as text
%        str2double(get(hObject,'String')) returns contents of edit2 as a double


% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3 as text
%        str2double(get(hObject,'String')) returns contents of edit3 as a double


% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
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



%SHIFT WAVE
% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs= global_data.fs;
shift1_const= str2double(get(handles.edit1,'string'));
shift2_const= str2double(get(handles.edit2,'string'));
[raw] = cam_formants(x, fs, 'ahdata');

f0_parameter = Harvest(x, fs);
spectrum_parameter = CheapTrick(x, fs, f0_parameter);
fft_size=spectrum_parameter.fft_size;
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;
source_parameter = D4C(x, fs, f0_parameter);
new_spectrogram= shiftwholewaveform(spectrum_parameter.spectrogram,raw, shift1_const, shift2_const,frequency_axis);
spectrum_parameter.spectrogram=new_spectrogram;

y = Synthesis(source_parameter, spectrum_parameter);
disp('done');
handles.player = audioplayer(y,fs);
handles.y=y;
handles.new_spectrogram=new_spectrogram;
handles.output = hObject;
guidata(hObject, handles);


%PLAY MODIFIED SOUND
% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
play(handles.player);

%WAVEFORM HEAT MAP
% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
new_spectrogram=handles.new_spectrogram;
HeatMap(new_spectrogram,'Colormap',parula, 'Standardize',2, 'DisplayRange', 1.6);
