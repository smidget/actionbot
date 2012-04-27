%include typemaps.i
%apply int &OUTPUT { int & result };
%module robochair
%{
#include "RoboteqDevice.h"
#include "Constants.h"
#include "ErrorCodes.h"
%}

%include "RoboteqDevice.h"
%include "Constants.h"
%include "ErrorCodes.h"
