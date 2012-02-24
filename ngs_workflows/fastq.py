#!/usr/bin/env python

#    This file is part of ngs_workflow.
#
#    ngs_workflow is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    ngs_workflow is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with ngs_workflow.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, gzip

def fastq_format(fastqfile):
   '''
   read few quality lines of a fastq file and test the encoded
   number to determine the quality format.
   '''
   if fastqfile.endswith('.gz'):
      with gzip.open(fastqfile,'rb') as fastq:
         format = fastq_parse_format(fastq,1200)
         # few became 1200, due to DNASeq data which might have
         # a lot of N at the beginning. Hopefully RNASeq don't..
   else:
      with open(fastqfile,'rb') as fastq:
         format = fastq_parse_format(fastq,1200)
   return fastq_range(format)

def fastq_parse_format(fastqfileobj,n_seq):
   '''
   It reads the first n_seq quality lines
   ad consider the max and min value
   '''
   n        = 0
   q_range = {'min':1000,'max':0}
   quality_list = False
   for line in fastqfileobj:
      if quality_list:
         q_line = [ord(val) for val in list(line.strip())]
         n +=1
         if max(q_line) > q_range['max']:
            q_range['max'] = max(q_line)
         if min(q_line) < q_range['min']:
            q_range['min'] = min(q_line)
         if n == n_seq:
            break
         quality_list = False
      else:
         if line.startswith('+'):
            quality_list = True
         else:
            pass
   return q_range

def fastq_range(min_max_dict):
   '''
   Look if the given min max dictionary is in range of
   Solexa/Illumina or Sanger fastq quality score.
   '''
   sanger     = {'min':33,'max':73}
   illumina13 = {'min':64,'max':104}
   illumina15 = {'min':67,'max':104}
   solexa     = {'min':59,'max':104}
   # Waste of lines I'll just chek if it's sanger, otherwise
   # return illumina... range 33-59 is sanger for sure;
   # 59-73 is ambiguous but probably sanger,
   # otherwhise is illumina
   if min_max_dict['min'] < 59:
      return "sanger"
   elif min_max_dict['min'] >= 59 and min_max_dict['max'] <= 73:
      return "sanger"
   elif min_max_dict['max'] > 73:
      return "illumina"
