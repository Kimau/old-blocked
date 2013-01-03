
//====================================================================================================
//                    _   _      _                   _____                 _   _                 
//                   | | | | ___| |_ __   ___ _ __  |  ___|   _ _ __   ___| |_(_) ___  _ __  ___ 
//                   | |_| |/ _ \ | '_ \ / _ \ '__| | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
//                   |  _  |  __/ | |_) |  __/ |    |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
//                   |_| |_|\___|_| .__/ \___|_|    |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
//                                |_|                                                            
//=====================================================================================================
/*jshint multistr:true */
/*jshint sub:true */
/*jshint browser:true */


function $(id) { return document.getElementById(id); }
function rgb(x) { return 'rgb(' + Math.floor(x[0] * 255) + ',' + Math.floor(x[1] * 255) + ',' + Math.floor(x[2] * 255) + ')'; }
function rgba(x) { return 'rgba(' + Math.floor(x[0] * 255) + ',' + Math.floor(x[1] * 255) + ',' + Math.floor(x[2] * 255) + ',' + x[3] + ')'; }
function toCssCol(x) { return (x.length < 4) ? rgb(x) : rgba(x); }
function argToParams(args) { return '?' + JSON.stringify(args).replace(new RegExp('[{}"]', 'g'), '').replace(new RegExp(':', 'g'), '=').replace(new RegExp(',', 'g'), '&'); }

function aHex(x, i) 
{
  var h = x.toString(16);
  while (h.length < i)
    h = '0' + h;

  return h.toUpperCase();
}

function BitsToBig(x, num) 
{
  var c = 0;
  var s = [];
  
  for (var i = 0; i < x.length; ++i) 
  {
    if (x[i] >= num) 
    {
      s = s.concat(c);
      c = 0;
    } 
    else 
    {
      c = c * num + x[i];
    }
  }
  
  if (c > 0)
    s = s.concat(c);
  else if (s.length === 0)
    s = [0];
  
  return s;
}

function MakeBit(x, num, padSize) 
{
  var y = [];
  
  if (x === 0)
    y = [0];
  
  while (x > 0) 
  {
    var r = x % num;
    y = y.concat(r);
    x = Math.floor(x / num);
  }
  
  if (padSize) 
  {
    while (y.length < padSize) 
    {
      y = y.concat(0);
    }
  }
  
  y = y.reverse();
  return y;
}

function BigToBits(x, num) 
{
  var y = [];
  for (var i = 0; i < x.length; ++i) 
  {
    if (i !== 0)
      y = y.concat(num);
    
    y = y.concat(MakeBit(x[i], num));
  }
  
  return y;
}

function StepDown(numSteps, mod) 
{
  var sDiff = Math.ceil(100 / (numSteps - 1));
  
  var i = 0;
  var steps = [100];
  while (steps[steps.length - 1] > sDiff) 
  {
    var x = steps[steps.length - 1] - sDiff;
    if (mod && ((i % mod) === 0))
      x += Math.floor(sDiff / 2);
    
    steps = steps.concat(x);
    ++i;
  }
  
  steps = steps.concat(0);
  
  if (mod === undefined)
    mod = 1;
  
  if (steps.length != numSteps) 
  {
    if (mod < numSteps)
      return StepDown(numSteps, mod + 1);
    else
      throw 'Cant Handle Steps';
  }
  
  return steps;
}

//----------------------------------------------------------------------------------
//                                     __     __         _ _     _           
//                                     \ \   / /_ _ _ __(_) |__ | | ___  ___ 
//                                      \ \ / / _` | '__| | '_ \| |/ _ \/ __|
//                                       \ V / (_| | |  | | |_) | |  __/\__ \
//                                        \_/ \__,_|_|  |_|_.__/|_|\___||___/
//                                                                           
//----------------------------------------------------------------------------------

var rawResponse;
var lastResponse;
var shadingMethods = {0: 'multiply',1: 'blend'};
var selectedBlot;

var currBlock = 
{
  'artistID': 0,
  'blockID': 0,
  'size': 8,
  'palColour': {'bits': 3,'colours': [[0, 0, 0], [1, 1, 1], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 0], [1, 0, 1], [0, 1, 1]]},
  'palAlpha': {'bits': 1,'scale': [100, 50]},
  'palShade': {'bits': 2,'colour': [0, 0, 0],'method': 0,'scale': [0, 33, 66, 100]},
  'palSmooth': {'bits': 0},
  
  'blkBits': [
    {'solidity': 1,'link': 0,'colour': 3,'alpha': 0,'shade': 0,'smooth': 0}, 
    {'solidity': 0,'link': [1, 2],'colour': 3}
  ]
};

// Temp Populate Function
currBlock.blkBits = [];
for (var i = 0; i < (currBlock.size * currBlock.size * currBlock.size); ++i) 
{
  var newBlock = {};
  
  newBlock.solidity = Math.floor(Math.random() * 2);
  newBlock.link = undefined;
  newBlock.colour = Math.floor(Math.random() * (Math.pow(2, currBlock.palColour.bits)));
  newBlock.alpha = Math.floor(Math.random() * (Math.pow(2, currBlock.palAlpha.bits)));
  newBlock.shade = Math.floor(Math.random() * (Math.pow(2, currBlock.palShade.bits)));
  newBlock.smooth = undefined;
  
  /* No more random links needed
  if (Math.random() < 0.25) 
  {
    newBlock.link = [Math.floor(Math.random() * 10000000), Math.floor(Math.random() * 50000)];
  } 
  else 
  {
    newBlock.link = undefined;
  }*/
  
  currBlock.blkBits = currBlock.blkBits.concat(newBlock);
}


//----------------------------------------------------------------------------------
//                                         _                _      
//                                        | |    ___   __ _(_) ___ 
//                                        | |   / _ \ / _` | |/ __|
//                                        | |__| (_) | (_| | | (__ 
//                                        |_____\___/ \__, |_|\___|
//                                                    |___/        
//----------------------------------------------------------------------------------
function BitMapForBlockBit(block)
{
  var b = 2;
  var x =[['solidity', 1],['link',1]];

  if (block.palColour && block.palColour.bits)
  {
    x = x.concat([['colour',block.palColour.bits]]);
    b += block.palColour.bits;
  }
  
  if (block.palAlpha && block.palAlpha.bits)
  {
    x = x.concat([['alpha',block.palAlpha.bits]]);
    b += block.palAlpha.bits;
  }
  
  if (block.palShade && block.palShade.bits)
  {
    x = x.concat([['shade',block.palShade.bits]]);
    b += block.palShade.bits;
  }
  
  if (block.palSmooth && block.palSmooth.bits)
  {
    x = x.concat([['smooth',block.palSmooth.bits]]);
    b += block.palSmooth.bits;
  }

  if(b < 8)
    x = x.concat([['',8 - b]]);

  return x.reverse();
}

function NumBitsPerBlockBit(block) 
{
  var x = 2;
  if (block.palColour && block.palColour.bits)
    x += block.palColour.bits;
  
  if (block.palAlpha && block.palAlpha.bits)
    x += block.palAlpha.bits;
  
  if (block.palShade && block.palShade.bits)
    x += block.palShade.bits;
  
  if (block.palSmooth && block.palSmooth.bits)
    x += block.palSmooth.bits;
  
  return x;
}

function BlockBitToBytes(block, bit) 
{
  var limit;
  var x = (bit.solidity) ? 1 : 0 + (bit.link) ? 2 : 0;
  var c = 2;
  
  if (block.palColour && block.palColour.bits) 
  {
    limit = Math.pow(2, block.palColour.bits);
    if (bit.colour >= limit) 
    {
      bit.colour = bit.colour % limit;
      console.warn('Colour out of Range');
    }
    
    x += bit.colour << c;
    c += block.palColour.bits;
  }
  
  if (block.palAlpha && block.palAlpha.bits) 
  {
    limit = Math.pow(2, block.palAlpha.bits);
    if (bit.alpha >= limit) 
    {
      bit.alpha = bit.alpha % limit;
      console.warn('Alpha out of Range');
    }
    
    x += bit.alpha << c;
    c += block.palAlpha.bits;
  }
  
  if (block.palShade && block.palShade.bits) 
  {
    limit = Math.pow(2, block.palShade.bits);
    if (bit.shade >= limit) 
    {
      bit.shade = bit.shade % limit;
      console.warn('Shade out of Range');
    }
    
    x += bit.shade << c;
    c += block.palShade.bits;
  }
  
  if (block.palSmooth && block.palSmooth.bits) 
  {
    limit = Math.pow(2, block.palSmooth.bits);
    if (bit.shade >= limit) 
    {
      bit.shade = bit.shade % limit;
      console.warn('Smooth out of Range');
    }
    
    x += bit.smooth << c;
    c += block.palSmooth.bits;
  }
  
  if (c >= 256) 
  {
    console.warn('Out of 8bit Range: ' + x);
  }
  
  return x;
}

// Artist        Block          Size  Colour               Alpha      Shade                   Smooth
// [AA AA AA AA] [BB BB BB BB]  ZZ    XX[[FF FF FF] x 32]  XX[FFx16]  XX[ MM FF FF FF FFx16]  XX
function PalToBytes(block) 
{
  var bits;
  var reqLen;
  var i;
  var palBytes = [];
  
  palBytes = palBytes.concat(MakeBit(block.artistID, 255, 4));
  palBytes = palBytes.concat(MakeBit(block.blockID, 255, 4));
  palBytes = palBytes.concat(block.size);

  // Process Colour Pallete
  if (block.palColour) 
  {
    bits = (block.palColour.bits) ? (block.palColour.bits) : 0;
    reqLen = Math.pow(2, bits);
    
    if (block.palColour.colours.length > reqLen)
      block.palColour.colours = block.palColour.colours.slice(0, reqLen);
    else
      while (block.palColour.colours.length < reqLen)
        block.palColour.colours = block.palColour.colours.concat([[0, 0, 0]]);

    // Add Data
    palBytes = palBytes.concat(10 + bits);
    for (i = 0; i < reqLen; i++) 
    {
      palBytes = palBytes.concat([
        block.palColour.colours[i][0] * 255, 
        block.palColour.colours[i][1] * 255, 
        block.palColour.colours[i][2] * 255]);
    }
  }

  // Process Alpha
  if (block.palAlpha) 
  {
    bits = (block.palAlpha.bits) ? (block.palAlpha.bits) : 0;
    reqLen = Math.pow(2, bits);
    
    if (block.palAlpha.scale.length > reqLen)
      block.palAlpha.scale = block.palAlpha.scale.slice(0, reqLen);
    else
      while (block.palAlpha.scale.length < reqLen)
        block.palAlpha.scale = block.palAlpha.scale.concat(0);

    // Add Data
    palBytes = palBytes.concat(20 + bits);
    palBytes = palBytes.concat(block.palAlpha.scale);
  }

  // Process Shading Pallette
  if (block.palShade) 
  {
    bits = (block.palShade.bits) ? (block.palShade.bits) : 0;
    reqLen = Math.pow(2, bits);
    
    if (block.palShade.scale.length > reqLen)
      block.palShade.scale = block.palShade.scale.slice(0, reqLen);
    else
      while (block.palShade.scale.length < reqLen)
        block.palShade.scale = block.palShade.scale.concat(0);

    // Add Data
    palBytes = palBytes.concat(30 + bits);
    palBytes = palBytes.concat(block.palShade.method);
    palBytes = palBytes.concat([
      block.palShade.colour[0] * 255, 
      block.palShade.colour[1] * 255, 
      block.palShade.colour[2] * 255]);
    
    palBytes = palBytes.concat(block.palShade.scale);
  }

  // Process Smoothing Pallette
  if (block.palSmooth) 
  {
    bits = (block.palSmooth.bits) ? (block.palSmooth.bits) : 0;
    palBytes = palBytes.concat(40 + bits);
  }
  
  return palBytes;
}

function BytesToPal(block, data) 
{
  block.artistID = BitsToBig(data.subarray(0, 4), 255)[0];
  block.blockID = BitsToBig(data.subarray(4, 4), 255)[0];
  block.size = data[8];
  
  block.palColour = undefined;
  block.palAlpha = undefined;
  block.palShade = undefined;
  block.palSmooth = undefined;
  
  // Process Pallettes
  var tmpData = data.subarray(9);
  var reqLen;
  var i;
  while (tmpData.length > 0) 
  {
    if ((tmpData[0] >= 10) && (tmpData[0] < 20)) 
    {
      // Colour
      block.palColour = {'bits': tmpData[0] % 10,'colours': []};
      
      tmpData = tmpData.subarray(1);
      reqLen = Math.pow(2, block.palColour.bits);
      for (i = 0; i < reqLen; i++)
        block.palColour.colours[i] = [tmpData[i * 3 + 0] / 255, tmpData[i * 3 + 1] / 255, tmpData[i * 3 + 2] / 255];
      
      tmpData = tmpData.subarray(reqLen * 3);
    } 
    else if ((tmpData[0] >= 20) && (tmpData[0] < 30)) 
    {
      // Alpha
      block.palAlpha = {'bits': tmpData[0] % 10,'scale': []};
      
      tmpData = tmpData.subarray(1);
      reqLen = Math.pow(2, block.palAlpha.bits);
      for (i = 0; i < reqLen; i++)
        block.palAlpha.scale[i] = tmpData[i];
      
      tmpData = tmpData.subarray(reqLen);
    } 
    else if ((tmpData[0] >= 30) && (tmpData[0] < 40)) 
    {
      // Shade
      block.palShade = {'bits': tmpData[0] % 10,'method': 0,'colour': [0, 0, 0],'scale': []};
      block.palShade.method = tmpData[1];
      block.palShade.colour = [tmpData[2] / 255, tmpData[3] / 255, tmpData[4] / 255];
      
      tmpData = tmpData.subarray(5);
      reqLen = Math.pow(2, block.palShade.bits);
      for (i = 0; i < reqLen; i++)
        block.palShade.scale[i] = tmpData[i];
      
      tmpData = tmpData.subarray(reqLen);
    } 
    else if ((tmpData[0] >= 40) && (tmpData[0] < 50)) 
    {
      // Smooth
      block.palSmooth = {'bits': tmpData[0] % 10};
      
      tmpData = tmpData.subarray(1);
    } 
    else 
    {
      throw "Unknown Pal or Something gone wrong in processing";
    }
  }
}

function BytesToBlkBit(block, data)
{
  var blkBit = {'solidity': (data & 1)};
  
  if (data & 2) 
  {
    blkBit.link = 1;
  }
  
  var c = 2;
  
  if (block.palColour && block.palColour.bits) 
  {
    blkBit.colour = (data >> c) % Math.pow(2, block.palColour.bits);
    c += block.palColour.bits;
  }
  
  if (block.palAlpha && block.palAlpha.bits) 
  {
    blkBit.alpha = (data >> c) % Math.pow(2, block.palAlpha.bits);
    c += block.palAlpha.bits;
  }
  
  if (block.palShade && block.palShade.bits) 
  {
    blkBit.shade = (data >> c) % Math.pow(2, block.palShade.bits);
    c += block.palShade.bits;
  }
  
  if (block.palSmooth && block.palSmooth.bits) 
  {
    blkBit.smooth = (data >> c) % Math.pow(2, block.palSmooth.bits);
    c += block.palSmooth.bits;
  }

  return blkBit;
}

function BytesToBlockBits(block, data) 
{
  block.blkBits = [];

  // Assume 8 bit MAX
  if (NumBitsPerBlockBit(block) > 8)
    throw "Too Many Bits for Block";

  // Copy Across Data
  for (var i = 0; i < data.length; i++) 
  {
    block.blkBits = block.blkBits.concat(BytesToBlkBit(block, data[i]));
  }
}

function BytesToLinks(block, data) 
{
  // Generating Flat List of ID
  var i;
  var flatIDList = [];
  
  for (i = 0; i < currBlock.blkBits.length; i++)
    if (block.blkBits[i].link)
      flatIDList = flatIDList.concat(i);

  // Decode Links
  var flatLinkDataList = BitsToBig(data, 255);
  
  for (i = 0; i < flatIDList.length; ++i)
    block.blkBits[flatIDList[i]].link = [flatLinkDataList[i * 2 + 0], flatLinkDataList[i * 2 + 1]];
}

function processMessage(e) 
{
  if (this.status == 200) 
  {
    var i;
    lastResponse = this;
    
    rawResponse = this.response;
    console.log(rawResponse);
    
    var szBlock = Number(this.getResponseHeader('szBlock'));
    var szPal = Number(this.getResponseHeader('szPal'));
    var szLink = Number(this.getResponseHeader('szLink'));
    
    var blockRecvData = new Uint8Array(rawResponse, 0, szBlock);
    var palRecvData = new Uint8Array(rawResponse, szBlock, szPal);
    var linkRecvData = new Uint8Array(rawResponse, szBlock + szPal, szLink);

    // Display Data
    $('blockRaw').innerHTML = '';
    for (i = 0; i < blockRecvData.length; i++) 
    {
      if (i > 0) 
      {
        if ((i % 8) === 0) 
        {
          $('blockRaw').innerHTML += '\n';
          $('blockDisplay').innerHTML += '<br/>';
        }
        
        if ((i % 64) === 0) 
        {
          $('blockRaw').innerHTML += '\n';
          $('blockDisplay').innerHTML += '<hr/>';
        }
      }
      
      $('blockRaw').innerHTML += aHex(blockRecvData[i], 2) + ' ';
    }
    
    $('palRaw').innerHTML = '';
    for (i = 0; i < palRecvData.length; i++) 
    {
      if (i > 0) 
      {
        if ((i % 8) === 0)
          $('palRaw').innerHTML += '\n';
        if ((i % 64) === 0)
          $('palRaw').innerHTML += '\n';
      }
      
      $('palRaw').innerHTML += aHex(palRecvData[i], 2) + ' ';
    }

    // Convert Data
    currBlock = {};
    BytesToPal(currBlock, palRecvData);
    BytesToBlockBits(currBlock, blockRecvData);
    BytesToLinks(currBlock, linkRecvData);
    
    UpdatePalDisplay();
    UpdateCubeDisplay();
  }
}

function MakeBlockDomElem(blkBit,i) 
{
  var blk = document.createElement('span');
  blk.className = 'block';
  blk.id = 'BB' + i;

  var innerJsonDebug = document.createElement('em');
  innerJsonDebug.innerHTML = JSON.stringify(blkBit).replace(new RegExp('[",{}]', 'g'), ' ').replace(new RegExp(' :', 'g'), '&nbsp;');
  blk.appendChild(innerJsonDebug);
  
  if (blkBit.solidity) 
  {
    var colour = [1, 1, 1, 1];
    
    if (blkBit.colour && currBlock.palColour && currBlock.palColour.bits) 
    {
      colour[0] = currBlock.palColour.colours[blkBit.colour][0];
      colour[1] = currBlock.palColour.colours[blkBit.colour][1];
      colour[2] = currBlock.palColour.colours[blkBit.colour][2];
    }
    
    if (blkBit.shade && currBlock.palShade && currBlock.palShade.bits) 
    {
      var tint = currBlock.palShade.colour;
      var lvl = currBlock.palShade.scale[blkBit.shade] / 100;
      
      switch (currBlock.palShade.method) 
      {
        case 0: // Multiply
          colour[0] = colour[0] + (tint[0] - 1) * lvl * colour[0];
          colour[1] = colour[1] + (tint[1] - 1) * lvl * colour[1];
          colour[2] = colour[2] + (tint[2] - 1) * lvl * colour[2];
          break;
        case 1: // Blend
          colour[0] = colour[0] + (tint[0] - colour[0]) * lvl;
          colour[1] = colour[1] + (tint[1] - colour[1]) * lvl;
          colour[2] = colour[2] + (tint[2] - colour[2]) * lvl;
          break;
      }
    }
    
    if (blkBit.alpha && currBlock.palAlpha && currBlock.palAlpha.bits) 
    {
      colour[3] = currBlock.palAlpha.scale[blkBit.alpha]/100;
    }
    
    blk.style.setProperty('background-color', toCssCol(colour));
  }
  else 
  {
    blk.style.setProperty('border', '1px dashed #000');
  } 

  // Link
  if (blkBit.link) 
  {
    blk.classList.add('blkLink');
  }

  // Smoothing
  if (blkBit.smooth) 
  {
    blk.classList.add('blkSmooth');
  }

  // Add On Click
  var makeClickFunc = function(id){ return function(){SelectBlk(id);}; };
  blk.onclick = makeClickFunc(i);
  
  return blk;
}

function UpdatePalDisplay() 
{
  var b,i;
  var palDisplay = $('palDisplay');
  palDisplay.innerHTML = '';
  selectedBlot = undefined;

  // Update Pal Display
  var s = '';
  s += '<span class="artistID">Artist #' + currBlock.artistID + '</span>';
  s += '<span class="blockID">Block #' + currBlock.artistID + '</span>';

  var x = BitMapForBlockBit(currBlock);
  s += '<span class="bitsPerBlock"><b>Bits per Block</b>:';
  for(i=0; i<x.length;++i) 
    for(b=0; b < x[i][1]; ++b) 
      s += '<span class="bitmapblk ' + x[i][0] + '" ></span>';
  s += '</span>';

  s += '<div class="pal"><h3>Solidity  [<span class="bitmapblk solidity" ></span>]</h3>';
  s += '<span class="blot" onclick="' + "SelectBlot(this,'solidity',0);" + '" style="background-color: rgba(0,0,0,0);"></span>';
  s += '<span class="blot" onclick="' + "SelectBlot(this,'solidity',1);" + '" style="background-color: rgba(255,255,255,1);"></span>';
  s += '</div>';
  
  if (currBlock.palColour) 
  {
    s += '<div class="pal palColour">';
    s += '<h3>Colour Pallette  [';
    for(b=0; b < currBlock.palColour.bits; ++b) 
      s += '<span class="bitmapblk colour" ></span>';
    s += ']</h3>';

    for (i = 0; i < currBlock.palColour.colours.length; i++) 
    {
      s += '<span class="blot" onclick="' + "SelectBlot(this,'colour'," + i + ');" style="background-color:' + rgb(currBlock.palColour.colours[i]) + ';"></span>';
    }

    s += '</div>';
  }
  
  if (currBlock.palAlpha) 
  {
    s += '<div class="pal palAlpha">';
    s += '<h3>Alpha Pallette  [';
    for(b=0; b < currBlock.palAlpha.bits; ++b) 
      s += '<span class="bitmapblk alpha" ></span>';
    s += ']</h3>';

    for (i = 0; i < currBlock.palAlpha.scale.length; i++) 
    {
      s += '<span class="blot" onclick="' + "SelectBlot(this,'alpha'," + i + ');" style="background-color:' + rgba([0, 0, 0, currBlock.palAlpha.scale[i] / 100]) + ';"></span>';
    }

    s += '</div>';
  }
  
  if (currBlock.palShade) 
  {
    s += '<div class="pal palShade">';
    s += '<h3>Shading Pallette  [';
    for(b=0; b < currBlock.palShade.bits; ++b) 
      s += '<span class="bitmapblk shade" ></span>';
    s += ']</h3>';

    s += '<span class="method">' + shadingMethods[currBlock.palShade.method] + '</span>';
    for (i = 0; i < currBlock.palShade.scale.length; i++) 
    {
      s += '<span class="blot" onclick="' + "SelectBlot(this,'shade'," + i + ');" style="background-color:' + rgba([currBlock.palShade.colour[0], currBlock.palShade.colour[1], currBlock.palShade.colour[2], currBlock.palShade.scale[i] / 100]) + ';"></span>';
    }

    s += '</div>';
  }
  
  if (currBlock.palSmooth) 
  {
    s += '<div class="pal palSmooth">';
    s += '<h3>Smoothing Pallette  [';
    for(b=0; b < currBlock.palSmooth.bits; ++b) 
      s += '<span class="bitmapblk smooth" ></span>';
    s += ']</h3>';

    s += '</div>';
  }

  s += '<div class="pal"><h3>Link Pallette [<span class="bitmapblk link" ></span>]</h3>';
  s += '<span class="blot" onclick="' + "SelectBlot(this,'link',undefined);" + '" style="background-color: rgba(0,0,0,0);"></span>';
  s += '<span class="blot" onclick="GetAndSetLinkBlot(this);" style="background-color: rgba(255,255,255,1);"></span>';
  s += '<h4>Link to Artist:Cube</h4>';
  s += '<input id="artistLinkID" type="number" min="0" />:<input id="cubeLinkID" type="number" min="0" />';
  s += '</div>';
    
  palDisplay.innerHTML = s;
}

function GetAndSetLinkBlot(caller)
{
  var linkVal = [Number($("artistLinkID").value), Number($("cubeLinkID").value)];
  SelectBlot(caller, 'link', linkVal);  
  caller.innerHTML = linkVal[0] + ':' + linkVal[1];
}

function UpdateCubeDisplay() 
{
  // Update Cube Display
  var i;
  var blkDisplay = $('blockDisplay');
  
  var currLayer = document.createElement('div');
  currLayer.id = 'layer0';
  currLayer.className = 'layer';
  
  for (i = 0; i < currBlock.blkBits.length; i++) 
  {
    if (i === 0)
      blkDisplay.innerHTML = '';
    else if ((i % 64) === 0) 
    {
      blkDisplay.appendChild(currLayer);
      
      currLayer = document.createElement('div');
      currLayer.id = 'layer' + (i / 64);
      currLayer.className = 'layer';
    } 
    else if ((i % 8) === 0)
      currLayer.innerHTML += '<br />';

    currLayer.appendChild(MakeBlockDomElem(currBlock.blkBits[i],i));
  }

  blkDisplay.appendChild(currLayer);

  var makeClickFunc = function(i){ return function(){SelectBlk(i);}; };

  var blkElemList = blkDisplay.getElementsByClassName('block'); 
  for (i = 0; i < blkElemList.length; i++) 
  {
    blkElemList[i].onclick = makeClickFunc(i);
  }

  SelectLayer($('layerSlider').value);
}

function doJSSubmit() 
{
  // Assume 8bit max
  if (NumBitsPerBlockBit(currBlock) > 8)
    throw "Too Many Bits for Block";

  // Random Data
  var palBytes = PalToBytes(currBlock);
  var palSendData = new Uint8Array(palBytes.length);
  palSendData.set(palBytes);
  
  var flatLinkList = [];
  var blockSendData = new Uint8Array(currBlock.blkBits.length);
  
  for (var i = 0; i < currBlock.blkBits.length; i++) 
  {
    blockSendData[i] = BlockBitToBytes(currBlock, currBlock.blkBits[i]);
    
    if (currBlock.blkBits[i].link) 
    {
      flatLinkList = flatLinkList.concat(currBlock.blkBits[i].link);
    }
  }
  
  flatLinkList = BigToBits(flatLinkList, 255);
  var linkSendData = new Uint8Array(flatLinkList.length);
  linkSendData.set(flatLinkList);

  // Arguments
  var args = 
  {
    'szBlock': blockSendData.byteLength,
    'szPal': palSendData.byteLength,
    'szLink': linkSendData.byteLength
  };

  // Setup Transfer Data
  var bugger = new ArrayBuffer(blockSendData.byteLength + palSendData.byteLength + linkSendData.byteLength);
  var cpyBData = new Uint8Array(bugger, 0, blockSendData.length);
  var cpyPData = new Uint8Array(bugger, blockSendData.byteLength, palSendData.length);
  var cpyLData = new Uint8Array(bugger, blockSendData.byteLength + palSendData.byteLength, linkSendData.length);
  
  cpyBData.set(blockSendData);
  cpyPData.set(palSendData);
  cpyLData.set(linkSendData);
  
  console.log(blockSendData.byteLength + palSendData.byteLength + linkSendData.byteLength);
  console.log(blockSendData.length + palSendData.length + linkSendData.length);

  // Setup and Send
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/blockEditor' + argToParams(args), true);
  xhr.responseType = 'arraybuffer';
  xhr.setRequestHeader('Content-Type', 'application/octlet;base64');
  xhr.onload = processMessage;
  xhr.send(bugger);
}

function SelectLayer(x) 
{
  var layers = document.getElementsByClassName("layer");
  
  for (var i = 0; i < layers.length; ++i)
  {
    if (i == x)
    {
      layers[i].classList.remove('hidden');
      layers[i].classList.remove('faded');
    }
    else if (i < x)
    {
      layers[i].classList.remove('hidden');
      layers[i].classList.add('faded');
    }
    else
      layers[i].classList.add('hidden');
  }
}

function SelectBlot(caller, pal,val)
{
  selectedBlot = [pal, val];
  console.log('Selected Blot : ' + selectedBlot);

  var bList = document.getElementsByClassName('blot');
  for(var i=0; i< bList.length; ++i)
    bList[i].classList.remove('active');
  caller.classList.add('active');
}

function SelectBlk(id)
{
  var blk = $('BB' + id);

  if(selectedBlot)
  {
    currBlock.blkBits[id][selectedBlot[0]] = selectedBlot[1];
  }

  blk.parentElement.replaceChild(MakeBlockDomElem(currBlock.blkBits[id],id),blk);
}

//=========================================================================================================
//=========================================================================================================
//=========================================================================================================
//=========================================================================================================
//=========================================================================================================