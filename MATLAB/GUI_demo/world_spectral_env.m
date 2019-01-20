function varargout = world_spectral_env(varargin)
% WORLD_SPECTRAL_ENV MATLAB code for world_spectral_env.fig
%      WORLD_SPECTRAL_ENV, by itself, creates a new WORLD_SPECTRAL_ENV or raises the existing
%      singleton*.
%
%      H = WORLD_SPECTRAL_ENV returns the handle to a new WORLD_SPECTRAL_ENV or the handle to
%      the existing singleton*.
%
%      WORLD_SPECTRAL_ENV('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in WORLD_SPECTRAL_ENV.M with the given input arguments.
%
%      WORLD_SPECTRAL_ENV('Property','Value',...) creates a new WORLD_SPECTRAL_ENV or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before world_spectral_env_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to world_spectral_env_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help world_spectral_env

% Last Modified by GUIDE v2.5 18-Sep-2017 12:05:06

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @world_spectral_env_OpeningFcn, ...
                   'gui_OutputFcn',  @world_spectral_env_OutputFcn, ...
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


% --- Executes just before world_spectral_env is made visible.
function world_spectral_env_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to world_spectral_env (see VARARGIN)
% Choose default command line output for world_spectral_env
%handles.output = hObject;
global_data= getappdata(0,'WAV_DATA');
disp(global_data)
x=global_data.wav;

%%SET STRING FOR INFO
set(handles.text3,'String',['Filename: ',global_data.filename]);
set(handles.text4,'String',['Sampling Frequency(Hz):  ',num2str(global_data.fs)]);
set(handles.text6,'String',['Audio Time length(s): ',num2str(length(x)/global_data.fs)]);

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes world_spectral_env wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = world_spectral_env_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
%varargout{1} = handles.output;



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

%PLOT AFTER ENTERING START TIME 
% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs=  global_data.fs;
filename = global_data.filename;
f0_parameter=global_data.f0_parameter;
time_pos= str2double(get(handles.edit1,'string'));
global_data.timepos=time_pos;
disp(time_pos);
spectrum_parameter=Cheap_Trick_Gui(x, fs, f0_parameter,time_pos);
set(handles.text5,'String',['FFT_Size:  ',num2str(spectrum_parameter.fft_size)]);
set(handles.text8,'String',['Frame length(ms):  ',num2str(length(spectrum_parameter.waveform)*1000/fs)]);
fft_size=spectrum_parameter.fft_size;
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;

%%%%plots DATA

axes(handles.axes1);
plot(spectrum_parameter.waveform)
disp(spectrum_parameter.waveform)
title('Waveform');
xlabel('No of Samples(s)');
ylabel('Amplitude');

axes(handles.axes2);
plot(frequency_axis(1:length(frequency_axis)),spectrum_parameter.power_spectrum)
title('Power Spectrum')
xlabel('frequency (Hz)');
ylabel('amplitude');

axes(handles.axes3);
plot([0;frequency_axis(1:length(frequency_axis)/2)],spectrum_parameter.smoothed_spectrum)
title('Smoothed Spectrum')
xlabel('frequency (Hz)');
ylabel('amplitude');


axes(handles.axes4);
hold off;
plot([0;frequency_axis(1:length(frequency_axis)/2)],20*log10(spectrum_parameter.spectral_envelope))
title('Spectral Envelope')
xlabel('frequency (Hz)');
ylabel('amplitude');
%pks=findpeaks(spectrum_parameter.spectral_envelope)
%[pks,locs]=findpeaks([0;frequency_axis(1:2:length(frequency_axis))],spectrum_parameter.spectral_envelope)







%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%CHEAP TRICK DATA
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% FORMANT TEST 1 CALLBACK GUI--- Executes on button press in checkbox1.
function checkbox1_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of checkbox1
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs=  global_data.fs;
filename = global_data.filename;
f0_parameter=global_data.f0_parameter;
time_pos= str2double(get(handles.edit1,'string'));
spectrum_parameter=Cheap_Trick_Gui(x, fs, f0_parameter,time_pos);
fft_size=spectrum_parameter.fft_size;
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;
axes(handles.axes4);
hold off;
plot([0;frequency_axis(1:length(frequency_axis)/2)],spectrum_parameter.spectral_envelope)
hold on;
metformants3(x, fs, filename)
outfile = ['out_',filename,'_formants.csv'];
[raw] = csvread(outfile);
time_array=raw(:,1);
for i=1:length(time_array)
    if time_pos  == time_array(i)
        vline(raw(i,3:end),'r:')
        %To include labels you might want to make it into  loop n
        %to vline each formant and write the frequencY
    end
end
title('Spectral Envelope F1')
xlabel('frequency (Hz)');
ylabel('amplitude');


% FORMANT TEST 2 CAM FORMANTS--- Executes on button press in checkbox2.
function checkbox2_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Defining Variables
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs=  global_data.fs;
filename = global_data.filename;
f0_parameter=global_data.f0_parameter;
time_pos= str2double(get(handles.edit1,'string'));
spectrum_parameter=Cheap_Trick_Gui(x, fs, f0_parameter,time_pos);
fft_size=spectrum_parameter.fft_size;
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;
axes(handles.axes4);
hold off;
plot([0;frequency_axis(1:length(frequency_axis)/2)],spectrum_parameter.spectral_envelope)
hold on;
[raw] = cam_formants(x, fs, filename);
time_array=raw(:,1);
for i=1:length(time_array)
    if  time_pos  == time_array(i)
        disp('formants 2')
        vline(raw(i,2:end),'b:')
    end
end
title('Spectral Envelope F2')
xlabel('frequency (Hz)');
ylabel('amplitude');

% Hint: get(hObject,'Value') returns toggle state of checkbox2


% FORMANT TEST 3--- Executes on button press in checkbox3.
function checkbox3_Callback(hObject, eventdata, handles)
% hObject    handle to checkbox3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs=  global_data.fs;
filename = global_data.filename;
f0_parameter=global_data.f0_parameter;
time_pos= str2double(get(handles.edit1,'string'));
spectrum_parameter=Cheap_Trick_Gui(x, fs, f0_parameter,time_pos);
fft_size=spectrum_parameter.fft_size;
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;
axes(handles.axes4);
hold off;
plot([0;frequency_axis(1:length(frequency_axis)/2)],spectrum_parameter.spectral_envelope)
hold on;
disp(spectrum_parameter.spectral_envelope)
[~, locs] = findpeaks(spectrum_parameter.spectral_envelope);
disp(locs)
vline(locs, 'g:')
title('Spectral Envelope Findpeaks')
xlabel('frequency (Hz)');
ylabel('amplitude');

% Hint: get(hObject,'Value') returns toggle state of checkbox3


