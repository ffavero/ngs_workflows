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

import rpy2.robjects as robjects
from   rpy2.robjects.packages import importr
import fastq_info

def fastq_adjust(filename,Ns=3,base_treshold=20):
   '''
   Reads the fastq file and adjust the reads quality
   '''
   shortread = importr('ShortRead')
   reads     = shortread.readFastq(filename)
   reads     = fastq_base_filter(reads,Ns=Ns,base_treshold=base_treshold)
   return

def fastq_base_filter(reads,Ns=3,base_treshold=20):
   '''
   It uses the ShortRead Bioconductr package and the
   rpy2 interface to filter the reads based on the nucleotides
   composition
   '''
   # Would be nice to do it like this:
   #filter1   = shortread.nFilter(threshold=Ns)
   #filter2   = shortread.polynFilter(threshold=base_treshold, nuc=robjects.vectors.StrVector("ACTG"))
   #filterall = shortread.compose(filter1,filter2)
   #idx_filt  = filterall(shortread.sread(reads))
   #reads     = reads.rx[idx_filt] ???? but the subscription does not works
   #Instead I would do like this.. for now:
   robjects.r('''
      basefilt <- function (reads, Ns, basetreshold) {
         require(ShortRead)
         filter1   <- nFilter(threshold=Ns)
         filter2   <- polynFilter(threshold=basetreshold, nuc=c("A","C","T","G"))
         filterall <- compose(filter1,filter2)
         reads[filterall(sread(reads))]
      }
   ''')
   return robjects.r['basefilt'](reads,Ns,base_treshold)
